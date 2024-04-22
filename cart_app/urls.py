from . import views
from django.urls import path

app_name = "cart_app"
urlpatterns = [
    path("cart_page", views.cart_page, name="cart_page"),
    path("add-to-cart/<int:pk>", views.add_cart, name="add-to-cart"),
    path("remove-from-cart/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("add-to-cart-store/<int:pk>/", views.add_cart_store, name="add_cart_store"),
    path("update/<int:pk>", views.cart_update, name="cart_update"),
    path("apply_coupon/<int:pk>", views.apply_coupon, name="apply_coupon"),
    path("checkout", views.checkout_page, name="checkout_page"),
    path("make_order", views.make_order, name="make_order"),
    path("orders", views.orders, name="orders"),
    path("order_detail/<int:pk>", views.order_detail, name="order_detail"),
    path("order_delete/<int:pk>", views.order_delete, name="order_delete"),
    path("order_item_delete/<int:pk>", views.order_item_delete, name="order_item_delete"),
    path("request_payment/<int:pk>", views.request_payment, name="request_payment"),
    path("verify_payment/<int:pk>", views.verify_payment, name="verify_payment"),
    path("filter_cities", views.filter_cities, name="filter_cities"),
    path("x", views.x, name="x"),
]
