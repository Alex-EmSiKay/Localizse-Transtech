import json
from random import choice
from datetime import datetime, timedelta
from uuid import uuid4

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q, F
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import (
    Language,
    TechContent,
    TechContentVersion,
    User,
    Item,
    Report,
    Message,
)
from .trnslt import tech_translate


@login_required
def accept(request, offer_id):
    if offer_id != request.user.offer:
        return HttpResponseRedirect(reverse("index"))
    else:
        request.user.groups.set([Group.objects.get(name="Auditor").pk])
        return HttpResponseRedirect(reverse("account"))


@login_required
def account(request):
    user_items = Item.objects.filter(user=request.user)
    audits = Item.objects.filter(
        work_type="AU",
        content__in=[i.content for i in user_items.filter(work_type="RE")],
    )
    num_audits = audits.count()
    num_flagged = audits.filter(~Q(final=F("initial"))).count()
    last_thursday = datetime.today() + timedelta(
        days=3 - datetime.today().weekday(), weeks=-1
    )
    weeks_items = Item.objects.filter(user=request.user, done__gt=last_thursday)
    SOFY = datetime(datetime.today().year, 7, 1)
    FYs_items = Item.objects.filter(user=request.user, done__gt=SOFY)
    return render(
        request,
        "transtech/account.html",
        {
            "primary_list": [lang.name for lang in request.user.primary.all()],
            "secondary_list": [lang.name for lang in request.user.secondary.all()],
            "work_log": user_items.order_by("-done")[:20],
            "num_audits": num_audits,
            "num_flagged": num_flagged,
            "accuracy": (num_audits - num_flagged) / num_audits * 100
            if num_audits != 0
            else 100,
            "languages": Language.objects.all(),
            "weekly": weeks_items.filter(work_type="RE").count() * 0.15
            + weeks_items.filter(work_type="AU").count() * 0.1,
            "FY": FYs_items.filter(work_type="RE").count() * 0.15
            + FYs_items.filter(work_type="AU").count() * 0.1,
            "locked": (timezone.now() - request.user.locked) < timedelta(days=7)
            if request.user.locked
            else False
            if request.user.locked
            else False,
        },
    )


def index(request):
    if request.user.is_authenticated:
        return render(request, "transtech/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def log(request):
    return render(
        request,
        "transtech/log.html",
        {
            "work_log": Item.objects.filter(user=request.user).order_by("-done"),
        },
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            if not user.active_pri:
                set_langs(user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "transtech/login.html")
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "transtech/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required
def messages(request):
    return render(
        request,
        "transtech/messages.html",
        {"messages": request.user.messages.all().order_by("-sent_at")},
    )


@login_required
def message(request, ID):
    msg = Message.objects.get(pk=ID)
    msg.read = True
    msg.save()
    return render(
        request,
        "transtech/message.html",
        {
            "message": msg,
            "content": msg.content.replace("\n", "<br>"),
        },
    )


@login_required
def offer(request):
    if request.user.is_staff and request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(pk=data.get("user_id"))
        user.offer = uuid4()
        user.save()
        Message.objects.create(
            recipient=user,
            subject="New Position Offer",
            content=f'You have been doing some great work and we would like to offer you a higher position.\nIf you are interested follow <a href="/accept/{user.offer}">this link</a>.',
        )
        return JsonResponse({"message": "Offered"}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def register(request):
    if request.method == "POST":
        username = request.POST["email"]
        email = request.POST["email"]
        name = request.POST["name"]
        primary = request.POST.getlist("primary")
        secondary = request.POST.getlist("secondary")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "transtech/register.html",
                {
                    "message": "Passwords must match.",
                    "languages": Language.objects.all(),
                },
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=name)
            user.save()
        except IntegrityError:
            return render(
                request,
                "transtech/register.html",
                {
                    "message": "email already registered.",
                    "languages": Language.objects.all(),
                },
            )
        for l in Language.objects.filter(code__in=primary):
            user.primary.add(l.pk)
        for l in Language.objects.filter(code__in=secondary):
            user.secondary.add(l.pk)
        user.groups.add(Group.objects.get(name="Reviewer"))
        login(request, user)
        set_langs(user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "transtech/register.html",
                {
                    "languages": Language.objects.all(),
                },
            )


@login_required
def report(request):
    # Saving new content must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        Report.objects.create(
            reporter=request.user,
            description=request.POST["description"],
            version=TechContentVersion.objects.get(pk=request.POST["version_id"]),
        )
        return HttpResponseRedirect(reverse("work"))


@login_required
def save(request):

    # Saving new content must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    lang = request.user.active_pri
    choices = [c for c in Language.objects.all()]
    if lang not in choices:
        return JsonResponse({"error": "not a valid language"}, status=400)
    cont = data.get("content")
    if data.get("content_id"):
        p_key = data.get("content_id")
        oldTC = TechContent.objects.get(pk=p_key)
        oldOriginal = TechContentVersion.objects.get(content_id=oldTC, language=lang)
        init = oldOriginal.content
        fin = cont
        oldOriginal.content = cont
        oldOriginal.save()
        if oldOriginal.version_type == "OR":
            for tr_lang in [c for c in choices if c != lang]:
                oldTranslation = TechContentVersion.objects.get(
                    content_id=oldTC, language=Language.objects.get(code=tr_lang)
                )
                oldTranslation.content = tech_translate(lang, tr_lang, cont)
                oldTranslation.save()
        if data.get("type"):
            if oldOriginal.status == "R":
                Item.objects.create(
                    user=request.user,
                    content=oldOriginal,
                    initial=init,
                    final=fin,
                    work_type="AU",
                )
                oldOriginal.status = "A"
                oldOriginal.save()
            if oldOriginal.status == "C":
                Item.objects.create(
                    user=request.user,
                    content=oldOriginal,
                    initial=init,
                    final=fin,
                    work_type="RE",
                )
                oldOriginal.status = "R"
                oldOriginal.save()

    else:
        newTC = TechContent.objects.create()
        p_key = newTC.pk
        newOriginal = TechContentVersion(
            content_id=newTC,
            language=lang,
            content=cont,
            version_type="OR",
            status="O",
        )
        newOriginal.save()
        for tr_lang in [c for c in choices if c != lang]:
            newTranslation = TechContentVersion(
                content_id=newTC,
                language=tr_lang,
                content=tech_translate(lang.code, tr_lang.code, cont),
                version_type="TR",
                status="C",
            )
            newTranslation.save()
    return JsonResponse(
        {"message": "Content saved successfully.", "content_id": p_key}, status=201
    )


@login_required
def set_lang(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    request.user.active_pri = Language.objects.get(code=data.get("primary"))
    request.user.active_sec = Language.objects.get(code=data.get("secondary"))
    request.user.save()
    return JsonResponse({"message": "Active languages saved successfully."}, status=201)


@login_required
def update(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    for field, val in data.get("info").items():
        if field == "primary":
            request.user.primary.set(
                [l.pk for l in Language.objects.filter(code__in=val)]
            )
        elif field == "secondary":
            request.user.secondary.set(
                [l.pk for l in Language.objects.filter(code__in=val)]
            )
        else:
            setattr(request.user, field, val)
    request.user.save()
    set_langs(request.user)
    return JsonResponse({"message": "Account updated successfully."}, status=201)


@login_required
def users(request):
    if request.user.is_staff:
        return render(
            request,
            "transtech/users.html",
            {"users": User.objects.filter(~Q(pk=request.user.pk))},
        )
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def work_switch(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse("index"))
    if request.user.groups.all()[0] == Group.objects.get(name="Creator"):
        return HttpResponseRedirect(reverse("work_by_type", args=["create"]))
    if request.user.groups.all()[0] == Group.objects.get(name="Reviewer"):
        return HttpResponseRedirect(reverse("work_by_type", args=["review"]))
    if request.user.groups.all()[0] == Group.objects.get(name="Auditor"):
        return HttpResponseRedirect(reverse("work_by_type", args=["audit"]))


@login_required
def work(request, w_type):
    if (
        (timezone.now() - request.user.locked) < timedelta(days=7)
        if request.user.locked
        else False
    ):
        return render(
            request, "transtech/workerror.html", {"type": w_type, "locked": True}
        )
    if w_type in [
        "create",
        "review",
        "audit",
    ]:
        if not request.user.is_staff:
            group = request.user.groups.all()[0]
            if not (
                (w_type == "create" and group.name == "Creator")
                or (w_type == "review" and group.name == "Reviewer")
                or (w_type == "audit" and group.name == "Auditor")
            ):
                return HttpResponseRedirect(reverse("work"))
        if w_type == "create":
            return render(request, f"transtech/{w_type}.html")
        else:
            clicks = [
                i.done
                for i in request.user.items.filter(
                    done__gt=timezone.now() - timedelta(days=7)
                ).order_by("-done")[:10]
            ]
            diffs = [(clicks[t] - clicks[t - 1]) for t in range(len(clicks) - 1)]
            if len([d for d in diffs if d < timedelta(seconds=3)]) > 2:
                request.user.locked = timezone.now()
                request.user.save()
                Message.objects.create(
                    recipient=request.user,
                    subject="Account locked",
                    content="We detected behaviour corresponding to fradulent activity. Your account has been locked for a week, please return then. Thank you.",
                )
                return HttpResponseRedirect(reverse("work"))
            print(clicks)
            translations = [
                c.content_id
                for c in TechContentVersion.objects.filter(
                    language=request.user.active_pri,
                    status=(
                        "C"
                        if w_type == "review"
                        else "R"
                        if w_type == "audit"
                        else None
                    ),
                )
            ]
            try:
                original = choice(
                    [
                        v
                        for v in TechContentVersion.objects.filter(
                            version_type="OR",
                            language=request.user.active_sec,
                            content_id__in=translations,
                        )
                        if v.reports.all().count() == 0
                    ]
                )
            except IndexError:
                return render(request, "transtech/workerror.html", {"type": w_type})

            translation = TechContentVersion.objects.get(
                content_id=original.content_id, language=request.user.active_pri
            )
            return render(
                request,
                f"transtech/{w_type}.html",
                {"original": original, "translation": translation},
            )
    else:
        return HttpResponseRedirect(reverse("index"))


def set_langs(user):
    user.active_pri = user.primary.all()[0]
    user.active_sec = [
        lang
        for lang in user.primary.all().union(user.secondary.all())
        if lang != user.active_pri
    ][0]
    user.save()
