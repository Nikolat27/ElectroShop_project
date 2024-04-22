from django.contrib import admin
from . import models


# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    inlines = (OrderItemInline,)


admin.site.register(models.Cart)
admin.site.register(models.Coupon)
admin.site.register(models.Refund)
admin.site.register(models.Province)
admin.site.register(models.City)
