from django.shortcuts import redirect

from cart_app.models import Cart
from product_app.models import Product


def context_processors(request):
    if request.user.is_authenticated is True:
        cart = Cart.objects.filter(user=request.user)

        cart_length = 0
        cart_total_price = 0
        total_len = 0

        for item in cart:
            cart_length = item.len(request)
            cart_total_price = item.total_cart_price(request)
            total_len = item.total_len(request)

        return {"cart": cart, "cart_length": cart_length, "cart_total_price": cart_total_price, "total_len": total_len}
    else:
        return {"hi": "asd"}
