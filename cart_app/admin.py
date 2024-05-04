from django.contrib import admin
from . import models


# Register your models here.
class CartItemInline(admin.TabularInline):
    model = models.CartItem


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    model = models.Cart
    inlines = (CartItemInline,)


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    inlines = (OrderItemInline,)


class CityInline(admin.TabularInline):
    model = models.City


@admin.register(models.Province)
class ProvinceAdmin(admin.ModelAdmin):
    model = models.Province
    inlines = (CityInline,)


admin.site.register(models.Coupon)
admin.site.register(models.Refund)
