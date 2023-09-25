import random
from datetime import datetime, timedelta
from uuid import uuid4
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User, OTP
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from . import forms
from random import randint
import ghasedakpack
from django.utils import timezone
from django.core.mail import send_mail

User = get_user_model()
sms = ghasedakpack.Ghasedak('71287bb24809cba0c9fc00e3697305b0ad3272bfe1b7d7946eb92c560931fc99')  # Api key code


# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home_app:main")

    form = forms.LoginForm(request.POST)
    next_page = request.GET.get("next")
    if form.is_valid():
        cd = form.cleaned_data
        phone = cd['phone']
        password = cd['password']

        user = authenticate(username=phone, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.info(request, f"You are now logged in as {phone}.")
        if next_page:
            return redirect(next_page)
        return redirect("home_app:main")
    return render(request, "account_app/login.html", context={"form": form})


def edit_page(request):
    if request.user.is_authenticated is None:
        return redirect("accounts_app:register_page")

    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        profile_picture = request.FILES.get("prof_pic")
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")

        user = request.user

        if username:
            user.username = username
        else:
            user.username = request.user.username

        user.prof_pic = profile_picture
        user.full_name = fullname
        user.email = email
        if password1 and password2:
            if password1 == password2:
                user.set_password(password1)

        user.save()
        return redirect("home_app:main")
    return render(request, "account_app/edit_form.html")


def change_password_page(request):
    if request.user.is_authenticated is None:
        return redirect("home_app:main")

    return render(request, "account_app/passwordchange.html")


def change_password(request):
    if request.user.is_authenticated is None:
        return redirect("home_app:main")

    if request.method == "POST":
        user = request.user
        newpass = random.randint(1000, 9999)
        subject = 'Password Change!'
        message = f"This is your new password = {newpass}"
        from_email = 'samalizadeh899@gmail.com'
        recipient_list = [user.email]
        user.set_password(str(newpass))
        user.save()
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse("Your password has been sended to your email and changed!")


def logout_page(request):
    logout(request)
    return redirect("home_app:main")


def otplogin(request):
    if request.method == "GET":
        form = forms.OtpLoginForm()
        return render(request, "account_app/register.html", {"form": form})

    if request.method == "POST":
        form = forms.OtpLoginForm(request.POST)
        if form.is_valid():
            randcode = randint(1000, 9999)
            cd = form.cleaned_data
            token = str(uuid4())
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            email = request.POST.get("email")

            if password1 == password2:     #Checking passwords
                email_check = User.objects.filter(email=email).exists()
                if email_check:
                    error = "This email exist`s !"          #Checking email
                    return render(request, "account_app/register.html", context={"errors": error, "form": form})
                else:
                    phone = User.objects.filter(phone=cd['phone']).exists()
                    if phone:
                        error = "This Phone number exist`s !"    #Checking the phonenumber
                        return render(request, "account_app/register.html", context={"errors": error, "form": form})
                    else:
                        OTP.objects.create(phone=cd['phone'], code=randcode, token=token, password=password1,
                                           email=email)
                        print(randcode)                 #And the last one , sending code to register the user!
                        return redirect(reverse("accounts_app:check_otp") + f"?token={token}")
            else:
                error = "Passwords are not same !"
                return render(request, "account_app/register.html", context={"errors": error})
            # sms.verification(
            #     {'receptor': cd["phone"], 'type': '1', 'template': 'websitecode', 'param1': randcode})
        else:
            form.add_error("phone", "invalid data")
        return render(request, "account_app/register.html", context={"form": form})


def otpcheck(request):
    if request.method == "GET":
        form = forms.CheckOtpForm()
        return render(request, "account_app/checkotp.html", {"form": form})

    if request.method == "POST":
        token = request.GET.get("token")
        form = forms.CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if OTP.objects.filter(code=cd['code'], token=token).exists():
                otp = OTP.objects.get(token=token)
                user = User.objects.create(phone=otp.phone, email=otp.email)

                password = otp.password
                user.set_password(password)
                user.save()

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                otp.delete()
                return redirect("home_app:main")

        else:
            form.add_error("code", "invalid data")

        return render(request, "account_app/checkotp.html", {"form": form})
