from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from cart_app.models import Cart
from product_app.models import Product


# Create your views here.

def ajax_template_generator(request, user):
    cart = Cart.objects.filter(user=user)
    cart_length = 0
    cart_total_price = 0
    total_len = 0

    for item in cart:
        cart_length = item.len(request)
        cart_total_price = item.total_cart_price(request)
        total_len = item.total_len(request)
    data = render_to_string("ajax_templates/cart_template_ajax.html",
                            context={"cart": cart, "cart_length": cart_length, "cart_total_price": cart_total_price,
                                     "total_len": total_len})
    return data


def add_cart(request, pk):
    if request.method == "POST":
        user = request.user
        product_id = pk
        color = request.POST.get("color")
        quantity = request.POST.get("quantity")

        if user and product_id and color and quantity:
            Cart.add(user=user, product_id=product_id, color=color, quantity=quantity)
            data = ajax_template_generator(request=request, user=user)
            return JsonResponse({"data": data, "bool": True})


def remove_from_cart(request, pk):
    user = request.user
    cart_id = pk
    if pk and user:
        Cart.remove_from_cart(user=user, cart_id=cart_id)
        data = ajax_template_generator(request=request, user=user)
        return JsonResponse({"data": data, "bool": True})
    else:
        return HttpResponse("error (pk and user)")


def add_cart_store(request, pk):
    user = request.user
    product_id = pk
    product = Product.objects.get(id=product_id)
    color = product.colors.first()
    print(color)
    if user and product:
        Cart.add(user=user, product_id=product_id, color=color, quantity=1)
        data = ajax_template_generator(request=request, user=user)
        return JsonResponse({"bool": True, "data": data})
