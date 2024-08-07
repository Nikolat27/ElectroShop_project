import json
import uuid

import requests
from random import randint
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from ElectroShop_project import settings
from account_app.models import User
from cart_app.models import Cart, Coupon, Order, OrderItem, City, Province, CartItem, Reserve
from product_app.models import Product, ProductColor
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


def ajax_template_generator(request, user=None, session_id=None):
    if user is not None:
        cart = Cart.objects.get(user=user)

    if session_id is not None:
        cart = Cart.objects.get(session_id=session_id)

    data = render_to_string("ajax_templates/cart_template_ajax.html",
                            context={"cart": cart})
    return data


def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.get("anonymous_user")
        cart = Cart.objects.filter(session_id=session_id).first()

    return render(request, "cart_app/cart_page.html", context={"cart": cart})


def add_cart(request, pk):
    if request.user.is_authenticated:
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
    else:
        session_id = request.session.get("anonymous_user")
        if session_id is None:
            session_id = str(uuid.uuid4())
            request.session['anonymous_user'] = session_id
            request.session.save()
            cart, created = Cart.objects.get_or_create(session_id=session_id)
        else:
            cart, created = Cart.objects.get_or_create(session_id=session_id)

    if request.method == "POST":
        product_id = pk
        color = request.POST.get("color")
        quantity = int(request.POST.get("quantity"))

        if product_id and color and quantity:
            product = Product.objects.get(id=product_id)

            # Check if the product already exists in the cart
            item, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color)
            if item:
                max_quantity = product.product_colors.filter(color__title__icontains=color).first().quantity
                # item.quantity is the value of quantity that user have been added in the PAST!
                # quantity is the value of quantity that user wants to add NOW!
                total_quantity = item.quantity + quantity
                if total_quantity < max_quantity:
                    item.quantity += quantity
                    if not item.price:
                        item.price = product.discount_price()

                    item.save()
                else:
                    # imagine 4 is the max_quantity and 2 is item.quantity(the value that we have added)
                    # 4 - 2 = remaining_quantity(2)
                    # item.quantity = item.quantity + 2(remaining_quantity)
                    remaining_quantity = max_quantity - item.quantity
                    item.quantity += remaining_quantity
                    item.save()

        if request.user.is_authenticated:
            data = ajax_template_generator(request=request, user=user)
        else:
            data = ajax_template_generator(request=request, session_id=session_id)

        return JsonResponse({"data": data, "bool": True})


def cart_update(request, pk):
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
    item = CartItem.objects.get(id=pk)
    item.delete()

    if request.user.is_authenticated:
        data = ajax_template_generator(request=request, user=request.user)
    else:
        session_id = request.session.get("anonymous_user")
        data = ajax_template_generator(request=request, session_id=session_id)

    return JsonResponse({"data": data, "bool": True})


def add_cart_store(request, pk):
    product = Product.objects.get(id=pk)
    color = product.product_colors.first().color.title
    max_quantity = product.product_colors.first().quantity

    if request.user.is_authenticated:
        # If user is authenticated, fetch the cart associated with the user
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.get("anonymous_user")
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session["anonymous_user"] = session_id
            request.session.save()
        # Fetch the cart associated with the session ID if user is not authenticated
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color)
    if cartitem.quantity < max_quantity:
        cartitem.price = product.discount_price()
        cartitem.quantity += 1
        cartitem.save()

        if request.user.is_authenticated:
            data = ajax_template_generator(request=request, user=request.user)
        else:
            data = ajax_template_generator(request=request, session_id=session_id)

        return JsonResponse({"data": data, "bool": True})


@login_required
def checkout_page(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
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
        province = request.POST.get("province")
        address = request.POST.get("address")
        postal_code = request.POST.get("postal_code")
        phone_number = request.POST.get("phone_number")
        optional_notes = request.POST.get("optional_notes")
        subtotal = request.POST.get("subtotal")
        order_code = randint(1000000000, 9999999999)
        order = Order.objects.create(user=user, first_name=fname, last_name=lname, email=email, city=city,
                                     province=province,
                                     address=address, postal_code=postal_code, phone_number=phone_number,
                                     optional_notes=optional_notes, subtotal=subtotal, order_code=order_code)

        user_cart = CartItem.objects.filter(cart__user=user)
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
    order = order_item.order
    next_page = request.GET.get("page_pk")
    order_item.delete()

    if not order.order_items.count() > 0:
        order.delete()
        return redirect("home_app:main")
    elif next_page:
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
                        if not order.coupon:
                            order.coupon_used = True
                            order.coupon = coupon
                            coupon.number_of_times_used += 1
                            order.calculate_subtotal()
                            order.save()
                            coupon.save()
                            return HttpResponse(
                                f"Your order`s subtotal considering %{coupon.discount_percentage} discount coupon: "
                                f"{order.subtotal}")
                        else:
                            return HttpResponse(f"You already have used your discount coupon!")

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


def check_reservation(request, pk):
    order = Order.objects.get(id=pk)

    with transaction.atomic():
        for item in order.order_items.all():
            if not check_and_reserve_product(request, item):
                reserve = Reserve.objects.filter(user=request.user)
                reserve.delete()
                return HttpResponse(f"Your product {item.product.title} "
                                    f"with color {item.color} is not available, Pls edit your basket")
            else:
                Reserve.objects.update_or_create(product=item.product, color=item.color,
                                                 defaults={'quantity': item.quantity}, user=request.user)

    return redirect(request_payment(request, order.id))


def check_and_reserve_product(request, item):
    # Get the Quantity of all the considered Product`s Reserves
    reserves = (Reserve.objects.filter(product=item.product, color__icontains=item.color, is_expired=False)
                .values_list("quantity", flat=True))
    # We need this queryset for inquiring the total quantity of the considered product with color
    product = ProductColor.objects.get(product=item.product, color__title__icontains=item.color)

    # Quantity amount that user wants to buy
    order_quantity = item.quantity

    # Calculating the Total Quantity which is Reserved by all users
    total_reserved = 0
    for reserve in reserves:
        total_reserved += reserve

    if total_reserved > 0:
        # (product.quantity) == The WHOLE quantity which is available
        # Total quantity which is available in the shop including reserves
        total_quantity = int(product.quantity) - int(total_reserved)

        # Check if user`s considered quantity is available in our shop or no (if is it, so user can buy)
        if order_quantity <= total_quantity:
            return True
        else:
            return False
    else:
        if order_quantity <= product.quantity:
            return True
        else:
            return False


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


def verify_payment(request):
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
            # Here if the payment was successful and
            # everything was ok we delete the product instance which was RESERVED
            reserved_product = Reserve.objects.get(reserved_id=123123)
            reserved_product.delete()

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
