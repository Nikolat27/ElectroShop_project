from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm


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
        if form.is_valid():
            return redirect("home_app:main")
    else:
        form = LoginForm(request=request)
    return render(request, "account_app/login.html", context={"form": form})


def logout_page(request):
    logout(request)
    return redirect("home_app:main")
