from django.urls import path
from . import views


app_name = "accounts_app"
urlpatterns = [
    path("register", views.otplogin, name="register_page"),
    path("edit", views.edit_page, name="edit_page"),
    path("logout", views.logout_page, name="logout_page"),
    path("login", views.login_page, name="login_page"),
    path("checkotp", views.otpcheck, name="check_otp"),
    path("passchange", views.change_password, name="pass_change"),
    path("passchangepage", views.change_password_page, name="pass_change_page"),
]
