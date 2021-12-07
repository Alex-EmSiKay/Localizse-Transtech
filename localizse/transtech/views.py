import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import TechContent, TechContentVersion, User


@login_required
def account(request):
    return render(request, "transtech/account.html", {"user_email": request.user.email})


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
    newTC = TechContent.objects.create()
    newTCV = TechContentVersion(
        content_id=newTC, language=data.get("language"), content=data.get("content")
    )
    newTCV.save()
    return JsonResponse({"message": "Content saved successfully."}, status=201)


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
            render(request, f"transtech/{type}.html")
        else:
            content = TechContent.objects.get(pk=4)
            original = TechContentVersion.objects.get(
                content_id=content, version_type="OR"
            )
            translation = TechContentVersion.objects.get(
                content_id=content, language="FR"
            )
            return render(
                request,
                f"transtech/{type}.html",
                {"original": original, "translation": translation},
            )
    else:
        return HttpResponseRedirect(reverse("index"))
