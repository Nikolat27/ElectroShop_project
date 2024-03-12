from django.contrib import admin
from . import models


# Register your models here.


class ImageInline(admin.TabularInline):
    model = models.Image


class SpecInline(admin.TabularInline):
    model = models.Specification


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    model = models.Category
    search_fields = ['title']
    autocomplete_fields = ['parent']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    model = models.Product
    inlines = [ImageInline, SpecInline]
    search_fields = ['title']
    list_display = ['title', "price", "show_image", "in_stock", "slug"]
    list_filter = ['in_stock']
    autocomplete_fields = ['category']


admin.site.register(models.Color)
admin.site.register(models.Comment)
admin.site.register(models.Brand)
admin.site.register(models.Ip)
