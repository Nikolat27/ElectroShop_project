from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, CaptchaTestForm, FormWithCaptcha
from .models import User


# Create your views here.


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            return redirect("account_app:login")
    else:
        form = RegisterForm()
    return render(request, "account_app/register.html", context={"form": form})


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST, request=request)
        form2 = FormWithCaptcha(request.POST)

        if form2.is_valid():
            if form.is_valid():
                return redirect("home_app:main")
        else:
            print("Captcha isn`t valid!")
    else:
        form = LoginForm(request=request)
        form2 = FormWithCaptcha()
    return render(request, "account_app/login.html", context={"form": form, "form2": form2})


def logout_page(request):
    logout(request)
    return redirect("home_app:main")