from django.shortcuts import redirect
from cart_app.models import Cart
from product_app.models import Product


def context_processors(request):
    if request.user.is_authenticated is True:
        cart1 = Cart.objects.filter(user=request.user)
        cart2 = Cart.objects.filter(user=request.user).first()
        if cart1 and cart2:
            cart_length = cart2.len(request)
            cart_total_price = cart2.total_cart_price(request)
            total_len = cart2.total_len(request)
        else:
            cart_length = 0
            cart_total_price = 0
            total_len = 0

        return {"cart": cart1, "cart_length": cart_length, "cart_total_price": cart_total_price, "total_len": total_len}
    else:
        cart_length = 0
        cart_total_price = 0
        total_len = 0
        return {"cart_length": cart_length, "cart_total_price": cart_total_price, "total_len": total_len}
