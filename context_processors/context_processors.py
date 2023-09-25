from cart_app.cart_function import Cart
from product_app.models import Product


def context_processors(request):
    products = Product.objects.filter(likes__user=request.user.id)
    cart = Cart(request)
    return {"cart": cart, "liked_products": len(products)}
