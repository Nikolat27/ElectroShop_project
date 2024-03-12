from . import views
from django.urls import path

app_name = 'account_app'
urlpatterns = [
    path("register", views.register_page, name="register"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout")
]
