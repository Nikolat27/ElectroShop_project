from django.shortcuts import redirect
from cart_app.models import Cart
from product_app.models import Product


def context_processors(request):
    if request.user.is_authenticated is True:
        user_cart = Cart.objects.filter(user=request.user).first()

        if user_cart:
            cart_length = user_cart.len()
            cart_total_price = user_cart.total_cart_price()
            total_quantity = user_cart.total_quantity()
        else:
            cart_length = 0
            cart_total_price = 0
            total_quantity = 0

        return {"cart": user_cart, "cart_length": cart_length, "cart_total_price": cart_total_price,
                "total_len": total_quantity}
    else:
        cart_length = 0
        cart_total_price = 0
        total_len = 0
        return {"cart_length": cart_length, "cart_total_price": cart_total_price, "total_len": total_len}
