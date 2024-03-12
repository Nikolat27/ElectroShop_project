from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect

from account_app.models import User
from product_app.models import Product


# Create your models here.


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_cart")
    color = models.CharField(max_length=40)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_products")

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
            return int(total)

    def total_cart_price(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user)
        total = 0
        for item in cart:
            total += item.total_item_price()
        return int(total)

    def remove_cart(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user)
        cart.delete()
        cart.save()
