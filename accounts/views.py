from src import settings
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib import messages
# Removed incorrect import of `request` from `requests` library
from .models import CustomUser
# Removed unused import
from django.core.mail import send_mail
 # Ensure settings is imported correctly


# Removed unused import
from django.contrib.auth import get_user_model
# from django.views.decorators.cache import cache_page
from django.shortcuts import render

# from django.core.cache import cache

from django.core.mail import EmailMultiAlternatives
# Removed unused import
from django.utils.html import strip_tags  # for email




# # Set
# cache.set('my_key', 'hello', timeout=60)  # 60 seconds

# # Get
# value = cache.get('my_key')  # 


#Getting user model
CustomUser = get_user_model()

def check_password_strength(password):
    # Check if the password is at least 8 characters long
    if len(password) < 8:
        return False
    return True
# Check if the password contains at least one digit










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

            if user:
                # ✅ Send HTML welcome email to user
                html_message = f"""
                <div style="max-width: 600px; margin: auto; padding: 20px; 
                            font-family: Arial, sans-serif; border: 1px solid #ddd; border-radius: 8px;">
                    <h2 style="color: #1E168FFF;">Welcome to Noahide Wisdom!</h2>
                    <p>Dear {fullname},</p>
                    <p>Thank you for signing up. We're excited to have you on board!</p>
                    <p>You can now login and explore our platform.</p>
                    <p style="text-align: center;">

                        <a href="{request.build_absolute_uri('signin')}" 
                           style="display: inline-block; padding: 10px 20px; color: #fff; 
                                  background-color: #1E168FFF; text-decoration: none; 
                                  border-radius: 5px;">Login</a>
                    </p>
                    <p>Warm regards,<br>The Noahide Wisdom Team</p>
                </div>
                """
                plain_text = strip_tags(html_message)

                welcome_email = EmailMultiAlternatives(
                    subject="Welcome to Noahide Wisdom",
                    body=plain_text,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                welcome_email.attach_alternative(html_message, "text/html")
                welcome_email.send()

                # ✅ Notify Admin/Owner
                # Notify Admin/Owner with styled email
                admin_html_message = f"""
                <div style="max-width: 600px; margin: auto; padding: 20px; 
                            font-family: Arial, sans-serif; border: 1px solid #ddd; border-radius: 8px;">
                    <h2 style="color: #1E168FFF;">New User Registration</h2>
                    <p>A new user has signed up on Noahide Wisdom:</p>
                    <ul>
                        <li><strong>Name:</strong> {fullname}</li>
                        <li><strong>Username:</strong> {username}</li>
                        <li><strong>Email:</strong> {email}</li>
                        <li><strong>Gender:</strong> {gender}</li>
                    </ul>
                    <p style="color: #555;">Please review the details and take any necessary actions.</p>
                </div>
                """
                admin_plain_text = strip_tags(admin_html_message)

                admin_email = EmailMultiAlternatives(
                    subject="New User Registered on Noahide Wisdom",
                    body=admin_plain_text,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL],  # Or ['admin@example.com']
                )
                admin_email.attach_alternative(admin_html_message, "text/html")
                admin_email.send()

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






















#Login
@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")





#Signin
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
# Profilre
@login_required(login_url="signin")
def profile(request, pk):
    user_profile = get_object_or_404(CustomUser, pk=pk)
    return render(request, "accounts/profile.html", {"user_profile": user_profile})




#Settings

@login_required(login_url="signin")
def setting(request):
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

    return render(request, "accounts/setting.html", {"user_profile": user_profile})