from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib import messages
# Removed incorrect import of `request` from `requests` library
from .models import CustomUser
import re

CustomUser = get_user_model()

def check_password_strength(password):
    # Check if the password is at least 8 characters long
    if len(password) < 8:
        return False
    return True

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        fullname = request.POST.get("fullname")
        gender = request.POST.get("gender")  # Capture gender
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match")
        elif not check_password_strength(password):
            messages.error(request, "Password is not strong enough")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email Taken")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username Taken")
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                fullname=fullname,
                gender=gender,  # Store gender
            )
            if user is not None:
                messages.success(request, "Account created successfully!")
                return redirect("signin")
            else:
                messages.error(request, "Failed to create account. Please try again later.")

        return render(
            request,
            "accounts/signup.html",
            {
                "username": username,
                "email": email,
                "fullname": fullname,
                "gender": gender,
            },
        )
    else:
        return render(request, "accounts/signup.html")



@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "accounts/signin.html", {"username": username})
    else:
        return render(request, "accounts/signin.html")


def profile(request, pk):
    user_profile = get_object_or_404(CustomUser, pk=pk)
    return render(request, "accounts/profile.html", {"user_profile": user_profile})


@login_required(login_url="signin")
@login_required(login_url="signin")
def settings(request):
    user_profile = request.user

    if request.method == "POST":
        fullname = request.POST.get("fullname", "")
        
        bio = request.POST.get("bio", "")

        user_profile.fullname = fullname
       
        user_profile.bio = bio

        if "profile_picture" in request.FILES:
            profile_picture = request.FILES["profile_picture"]
            user_profile.profile_picture = profile_picture

        user_profile.save()

        return redirect("profile", user_profile.pk)

    return render(request, "accounts/settings.html", {"user_profile": user_profile})