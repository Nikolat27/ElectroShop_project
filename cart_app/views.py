import json
import requests
from random import randint
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from MyEcommerce_project import settings
from account_app.models import User
from cart_app.models import Cart, Coupon, Order, OrderItem, City, Province, CartItem
from product_app.models import Product
from . import iran_province_city

# Create your views here.

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
# ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
# ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/"

phone = "09170910714"
description = "Hello World"
CallbackURL = "http://127.0.0.1:8000/cart/verify_payment"


def ajax_template_generator(request, user):
    cart = Cart.objects.filter(user=user).first()

    cart_length = cart.len()
    cart_total_price = cart.total_cart_price()
    total_quantity = cart.total_quantity()
    data = render_to_string("ajax_templates/cart_template_ajax.html",
                            context={"cart": cart, "cart_length": cart_length, "cart_total_price": cart_total_price,
                                     "total_len": total_quantity})
    return data


def cart_page(request):
    cart = Cart.objects.filter(user=request.user).first()

    return render(request, "cart_app/cart_page.html", context={"cart": cart})


def add_cart(request, pk):
    if request.user.is_authenticated is True:
        if request.method == "POST":
            user = request.user
            product_id = pk
            color = request.POST.get("color")
            quantity = int(request.POST.get("quantity"))

            if user and product_id and color and quantity:
                cart = Cart.objects.filter(user=user)
                product = Product.objects.get(id=product_id)

                if cart.exists():
                    # Check if the product already exists in the cart
                    item_exists = CartItem.objects.filter(cart=cart.first(), product=product, color=color)
                    if item_exists.exists():
                        item = item_exists.first()
                        item.quantity += quantity
                        item.save()
                        data = ajax_template_generator(request=request, user=user)
                        return JsonResponse({"data": data, "bool": True})
                    else:
                        CartItem.objects.create(cart=cart.first(), product=product, quantity=quantity, color=color,
                                                price=product.discount_price())
                        data = ajax_template_generator(request=request, user=user)
                        return JsonResponse({"data": data, "bool": True})
                else:
                    cart = Cart.objects.create(user=user)
                    CartItem.objects.create(cart=cart, product=product, quantity=quantity, color=color,
                                            price=product.discount_price())
                    data = ajax_template_generator(request=request, user=user)
                    return JsonResponse({"data": data, "bool": True})
    else:
        print("hi")


def cart_update(request, pk):
    if request.user.is_authenticated is True:
        new_quantity = int(request.GET.get("new_quantity"))
        if new_quantity and new_quantity >= 1:
            cart_item = CartItem.objects.get(id=pk)
            cart_item.quantity = new_quantity
            cart_item.save()
            new_price = cart_item.total_item_price()
            subtotal = cart_item.cart.total_cart_price()
            return JsonResponse({"bool": True, "new_price": new_price, "subtotal": subtotal})
        else:
            return JsonResponse({"bool": False})


def remove_from_cart(request, pk):
    user = request.user
    cart_item_id = pk
    if pk and user:
        item = CartItem.objects.get(id=cart_item_id)
        item.delete()
        data = ajax_template_generator(request=request, user=user)
        return JsonResponse({"data": data, "bool": True})
    else:
        return HttpResponse("error (pk and user)")


def add_cart_store(request, pk):
    user = request.user
    product_id = pk
    product = Product.objects.get(id=product_id)
    color = product.colors.first()
    if user and product:
        cart = Cart.objects.filter(user=user)
        # Check if the user has cart or no
        if cart.exists():
            # Check if the product already exists in the cart
            item_exists = CartItem.objects.filter(cart=cart.first(), product=product, color=color,
                                                  price=product.discount_price())

            if item_exists.exists():
                item = item_exists.first()
                item.quantity += 1
                item.save()
                data = ajax_template_generator(request=request, user=user)
                return JsonResponse({"data": data, "bool": True})
            else:
                CartItem.objects.create(cart=cart.first(), product=product, quantity=1, color=color,
                                        price=product.discount_price())
                data = ajax_template_generator(request=request, user=user)
                return JsonResponse({"data": data, "bool": True})
        else:
            cart = Cart.objects.create(user=user)
            CartItem.objects.create(cart=cart, product=product, quantity=1, color=color,
                                    price=product.discount_price())
            data = ajax_template_generator(request=request, user=user)
            return JsonResponse({"data": data, "bool": True})


@login_required
def checkout_page(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    provinces = Province.objects.all()
    return render(request, "cart_app/checkout.html", context={"cart": cart,
                                                              "provinces": provinces})


def filter_cities(request):
    province = request.GET.get("province")
    cities = City.objects.filter(province__name=province).values("name")
    return JsonResponse({"bool": True, "data": list(cities)})


def make_order(request):
    if request.method == "POST":
        user = request.user
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        city = request.POST.get("city")
        country = request.POST.get("country")
        address = request.POST.get("address")
        postal_code = request.POST.get("postal_code")
        phone_number = request.POST.get("phone_number")
        optional_notes = request.POST.get("optional_notes")
        subtotal = request.POST.get("subtotal")
        order_code = randint(1000000000, 9999999999)
        order = Order.objects.create(user=user, first_name=fname, last_name=lname, email=email, city=city,
                                     country=country,
                                     address=address, postal_code=postal_code, phone_number=phone_number,
                                     optional_notes=optional_notes, subtotal=subtotal, order_code=order_code)

        user_cart = Cart.objects.filter(user=user)
        for item in user_cart:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, color=item.color,
                                     price=item.total_item_price())
            item.delete()
        order.calculate_subtotal()
        return redirect("cart_app:orders")


@login_required()
def orders(request):
    orders = Order.objects.filter(user=request.user)
    total = 0
    for order in orders:
        total += order.subtotal

    return render(request, "cart_app/orders_page.html", context={"orders": orders, "total": total})


def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    return render(request, "cart_app/order_detail.html", context={"order": order})


def order_delete(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect("cart_app:orders")


def order_item_delete(request, pk):
    order_item = OrderItem.objects.get(id=pk)
    next_page = request.GET.get("page_pk")
    order_item.delete()
    if next_page:
        return redirect("cart_app:order_detail", next_page)
    else:
        return redirect("home_app:main")


def apply_coupon(request, pk):
    coupon_code = request.GET.get("coupon_code")
    order = Order.objects.get(id=pk)
    if coupon_code:
        coupon = Coupon.objects.get(code=coupon_code)
        if coupon:
            if not coupon.expired and coupon.active:
                if coupon.limit_price <= order.subtotal <= coupon.maximum_price:
                    if coupon.maximum_use >= coupon.number_of_times_used:
                        order.coupon_used = True
                        coupon.number_of_times_used += 1
                        order.total_cart_price()
                        order.save()
                        coupon.save()
                        return HttpResponse(f"{order.subtotal}")
                    else:
                        print(f"You have reached to your maximum uses of this coupon ({coupon.maximum_use})")
                else:
                    print("Your Cart subtotal is lower than coupon`s limit price "
                          "or its greater than maximum")
            else:
                print("Coupon is Expired or unactivated")
        else:
            print("Coupon didnt find")
    else:
        print("No coupon")


def request_payment(request, pk):
    order = Order.objects.get(id=pk)
    subtotal = order.subtotal

    if subtotal == 0:
        return redirect(reverse('product_app:store_page'))
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": int(subtotal),
        "Description": description,
        "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response_x = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        print(response_x)
        if response_x.status_code == 200:
            print("It Works!!")
            parsed_response = response_x.json()
            if parsed_response['Status'] == 100:
                url = f"{ZP_API_STARTPAY}{parsed_response['Authority']}"
                print("It Works 2")
                return redirect(url)
            else:
                print("It does`nt work 2")
                return {'status': False, 'code': str(parsed_response['Status'])}
        else:
            print("It does`nt work")
            return response_x

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify_payment(request, pk):
    authority = request.GET['Authority']
    order = Order.objects.get(is_paid=False, user=request.user)
    subtotal = order.subtotal()
    user = User.objects.filter(id=request.user.id).first()
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": subtotal,
        'Authority': authority,

    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    res = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    if res.status_code == 200:
        response = res.json()

        if response['Status'] == 100:
            order.is_paid = True
            user.order_count += 1
            user.total_buy += subtotal

            user.save()
            order.save()
            return redirect(reverse('home_app:successful_payment_page'))

    return redirect(reverse('home_app:unsuccessful_payment_page'))


def x(request):
    data = iran_province_city.data

    # Create Province and City instances
    for province_data in data:
        province = Province.objects.create(name=province_data['name'])
        for city_data in province_data['cities']:
            City.objects.create(name=city_data['name'], province=province)
