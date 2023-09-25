from . import views
from django.urls import path

app_name = "cart_app"
urlpatterns = [
    path("add/<int:pk>", views.cartadd, name="cart_add"),
    path("delete/<str:id>", views.deletecart, name="delete_cart"),
    path("order/<int:pk>", views.order_detail, name="order_detail"),
    path("order/add", views.order_creation, name="order_creation"),
    path("add_address", views.address_creation, name="address"),
    path("cart_view", views.cart_view, name="cart_view"),
    path("cart_update/<int:pk>", views.cart_update, name="cart_update"),
    path("cart_delete/<str:id>", views.deletecart2, name="cart-delete-2"),
    path('apply/', views.couponapply, name='apply_coupon'),
]
