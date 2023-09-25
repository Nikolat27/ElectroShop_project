from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from product_app.models import Product
from .cart_function import Cart
from .forms import CouponApplyForm
from .models import Order, OrderItem, Address, Coupon


def cart_view(request):
    cart = Cart(request)
    form = CouponApplyForm(request.POST)
    return render(request, "product_app/view_cart.html", context={"cart_list": cart, "couponform": form})


@require_POST
@csrf_exempt
def cartadd(request, pk):
    if request.user.is_authenticated is False:
        return redirect("accounts_app:login_page")

    if request.method == "POST":
        product = get_object_or_404(Product, id=pk)
        color = request.POST.get("color")
        if not color:
            color = product.color.first().name
        size = request.POST.get("size")
        if not size:
            size = product.size.first().name
        override_quantity = request.POST.get("override")
        quantity = request.POST.get("quantity", "1")
        cart = Cart(request)
        cart.add(product, quantity, color, size, override_quantity=override_quantity)
        data = render_to_string("core/async/cart-detail.html", {"cart": cart}, request)

        return JsonResponse({'bool': True, "data": data, 'totalcartitems': int(cart.len())})


def cart_update(request, pk):
    if request.user.is_authenticated is False:
        return redirect("accounts_app:login_page")

    if request.method == "POST":
        product = get_object_or_404(Product, id=pk)
        color = request.POST.get("color")
        if not color:
            color = product.color.first().name
        size = request.POST.get("size")
        if not size:
            size = product.size.first().name
        override_quantity = request.POST.get("override")
        quantity = request.POST.get("quantity", "1")
        cart = Cart(request)
        cart.add(product, quantity, color, size, override_quantity=override_quantity)
        data = render_to_string("core/async/cart-list.html", {"cart_list": cart}, request)
        data2 = render_to_string("core/async/cart-detail.html", {"cart": cart})

        return JsonResponse({'bool': True, "data": data, "data2": data2, 'totalcartitems': int(cart.len())})


def deletecart(request, id):
    if request.user.is_authenticated is False:
        return redirect("accounts_app:login_page")
    cart = Cart(request)
    cart.delete(id=id)
    data = render_to_string("core/async/after-cart-delete.html", {"cart": cart})

    return JsonResponse({"bool": True, "data": data, "totalcartitems": int(cart.len())})


def deletecart2(request, id):
    if request.user.is_authenticated is False:
        return redirect("accounts_app:login_page")
    cart = Cart(request)
    cart.delete(id=id)
    cart = Cart(request)

    data = render_to_string("core/async/after-cart-delete-2.html", {"cart_list": cart, "cart": cart})
    cart_view_data = render_to_string("core/async/after-cart-delete.html", {"cart": cart})
    return JsonResponse({'bool': True, 'data': data, "data2": cart_view_data, "totalcartitems": int(cart.len())})


def order_detail(request, pk):
    if request.user.is_authenticated is False:
        return redirect("accounts_app:login_page")

    order = Order.objects.get(id=pk)
    return render(request, "cart_app/checkout.html", context={"order": order})


def order_creation(request):
    if request.user.is_authenticated is False:
        return redirect("accounts_app:login_page")

    cart = Cart(request)
    order = Order.objects.create(user=request.user, total_price=int(cart.total()))
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], color=item['color'], size=item['size'],
                                 quantity=item['quantity'], price=item['price'])

    # cart.remove_cart()
    return redirect("cart_app:order_detail", order.id)


def address_creation(request):
    if request.method == "POST":
        full_name = request.POST.get("full-name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        postal_code = request.POST.get("postal-code")
        city = request.POST.get("city")

        Address.objects.create(full_name=full_name, email=email, phone=phone, address=address, city=city,
                               postal_code=postal_code, user=request.user)
        next_page = request.GET.get("next")
        if next_page:
            return redirect(next_page)

    return render(request, "cart_app/checkout.html")


def couponapply(request):
    if request.method == "POST":
        now = timezone.now()
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
                request.session['coupon_id'] = coupon.id
                print("coupon added successfully")
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
                print("coupon`s code is wrong")
        return redirect('cart_app:cart_list')
