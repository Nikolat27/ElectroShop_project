from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.shortcuts import get_object_or_404, redirect
from account_app.models import User
from product_app.models import Product
from datetime import datetime
from django.utils import timezone


# Create your models here.


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_cart")
    color = models.CharField(max_length=40)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_products")
    coupon_used = models.FloatField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.product.title} - {self.user.username}"

    @classmethod
    def add(self, user, product_id, color, quantity):
        product = get_object_or_404(Product, id=product_id)
        have_cart = False
        try:
            user_cart = Cart.objects.get(user=user, product=product, color=color)
            if user_cart:
                have_cart = True
        except:
            have_cart = False

        if have_cart is True:
            new_quantity = int(quantity)
            user_cart.quantity += new_quantity
            user_cart.save()  # Allways remember to save your changes!
        else:
            Cart.objects.create(user=user, product=product, color=color, quantity=quantity)

    @classmethod
    def remove_from_cart(self, cart_id, user):
        cart = Cart.objects.get(user=user, id=cart_id)
        if cart:
            cart.delete()
        else:
            print("no cart")

    def len(self, request):
        user = request.user
        cart_total = Cart.objects.filter(user=user).count()
        return cart_total

    def total_len(self, request):
        user = request.user
        cart_total = Cart.objects.filter(user=user)
        total_quantity = 0
        for item in cart_total:
            total_quantity += item.quantity
        return total_quantity

    def total_item_price(self):
        if self.product and self.quantity:
            total = self.product.discount_price() * self.quantity
            return float(total)

    def total_cart_price(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user)
        subtotal = 0
        for item in cart:
            subtotal += item.total_item_price()
        return subtotal

    def remove_cart(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user)
        cart.delete()


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    limit_price = models.IntegerField(default=10)
    maximum_price = models.IntegerField(default=1000000)
    valid_from = models.DateTimeField(auto_now=False, verbose_name="Start at")
    valid_to = models.DateTimeField(auto_now=False, verbose_name="Expire at")
    active = models.BooleanField(help_text="If you wanna this coupon be available tick this field")
    expired = models.BooleanField(default=False, editable=False)
    maximum_use = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.make_aware(datetime.now())
        if self.valid_from and self.valid_to:
            if (now < self.valid_from) or (now > self.valid_to):
                self.expired = True
                self.save()
            else:
                self.expired = False
                self.save()


order_choices = (("unpaid", "unpaid"), ("paid", "paid"), ("refund", "refund"))


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    postal_code = models.IntegerField()
    phone_number = models.CharField(max_length=11)
    subtotal = models.FloatField()
    is_paid = models.BooleanField(default=False)
    status = models.CharField(choices=order_choices, max_length=20, default="unpaid")
    order_code = models.CharField(max_length=20, unique=True)
    optional_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon_used = models.BooleanField(default=False)
    coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE, null=True, blank=True)

    def calculate_subtotal(self):
        order_items = self.order_items.all()
        total = 0
        for item in order_items:
            total += item.price

        if self.coupon_used is True:
            discount_amount = (self.coupon.discount_percentage / 100) * total
            total -= discount_amount
            self.subtotal = total
        else:
            self.subtotal = total
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.city} - {self.subtotal} - {self.is_paid} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    color = models.CharField(max_length=30)
    quantity = models.IntegerField(default=1)
    price = models.BigIntegerField()

    def __str__(self):
        return f"{self.order.user.username} - {self.product.title} - {self.price} - {self.order.is_paid}"


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="refund_order")
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2)
    refund_reason = models.TextField(null=True, blank=True)
    refunded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} - {self.refund_amount} - {self.refunded_at.day}"


class Province(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
