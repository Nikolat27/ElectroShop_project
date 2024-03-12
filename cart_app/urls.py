from . import views
from django.urls import path

app_name = "cart_app"
urlpatterns = [
    path("add-to-cart/<int:pk>", views.add_cart, name="add-to-cart"),
    path("remove-from-cart/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("add-to-cart-store/<int:pk>/", views.add_cart_store, name="add_cart_store"),
]
