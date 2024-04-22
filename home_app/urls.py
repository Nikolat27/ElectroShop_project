from . import views
from django.urls import path

app_name = "home_app"
urlpatterns = [
    path("", views.home_page, name="main"),
    path("successful_payment_page", views.successful_payment_page, name="successful_payment_page"),
    path("unsuccessful_payment_page", views.unsuccessful_payment_page, name="unsuccessful_payment_page"),
]
