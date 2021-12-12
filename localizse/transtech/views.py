import json
from random import choice

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Language, TechContent, TechContentVersion, User
from .trnslt import tech_translate


@login_required
def account(request):
    return render(
        request,
        "transtech/account.html",
        {
            "user_email": request.user.email,
            "primary_list": [lang.name for lang in request.user.primary.all()],
            "secondary_list": [lang.name for lang in request.user.secondary.all()],
        },
    )


def index(request):
    if request.user.is_authenticated:
        return render(request, "transtech/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def finance(request):
    pass


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
                user.active_pri = user.primary.all()[0]
                user.active_sec = [
                    lang
                    for lang in user.primary.all().union(user.secondary.all())
                    if lang != user.active_pri
                ][0]
                user.save()
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
    return render(request, "transtech/messages.html")


def register(request):
    if request.method == "POST":
        username = request.POST["email"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "transtech/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "transtech/register.html",
                {"message": "email already registered."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "transtech/register.html")


@login_required
def save(request):

    # Saving new content must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    lang = data.get("language")
    choices = [c.code for c in Language.objects.all()]
    if lang not in choices:
        return JsonResponse({"error": "not a valid language"}, status=400)
    cont = data.get("content")
    if data.get("content_id"):
        p_key = data.get("content_id")
        oldTC = TechContent.objects.get(pk=p_key)
        oldOriginal = TechContentVersion.objects.get(
            content_id=oldTC, language=Language.objects.get(code=lang)
        )
        oldOriginal.content = cont
        oldOriginal.save()
        if oldOriginal.version_type == "OR":
            for tr_lang in [c for c in choices if c != lang]:
                oldTranslation = TechContentVersion.objects.get(
                    content_id=oldTC, language=Language.objects.get(code=tr_lang)
                )
                oldTranslation.content = tech_translate(lang, tr_lang, cont)
                oldTranslation.save()
    else:
        newTC = TechContent.objects.create()
        p_key = newTC.pk
        newOriginal = TechContentVersion(
            content_id=newTC,
            language=Language.objects.get(code=lang),
            content=cont,
            version_type="OR",
            status="O",
        )
        newOriginal.save()
        for tr_lang in [c for c in choices if c != lang]:
            newTranslation = TechContentVersion(
                content_id=newTC,
                language=Language.objects.get(code=tr_lang),
                content=tech_translate(lang, tr_lang, cont),
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
def work_switch(request):
    return HttpResponseRedirect(reverse("index"))


@login_required
def work(request, type):
    if type in [
        "create",
        "review",
        "audit",
    ]:
        if type == "create":
            return render(request, f"transtech/{type}.html")
        else:
            original = choice(
                TechContentVersion.objects.filter(
                    version_type="OR", language=request.user.active_sec
                )
            )
            translation = TechContentVersion.objects.get(
                content_id=original.content_id, language=request.user.active_pri
            )
            return render(
                request,
                f"transtech/{type}.html",
                {"original": original, "translation": translation},
            )
    else:
        return HttpResponseRedirect(reverse("index"))
