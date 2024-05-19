from django.contrib import admin
from . import models


# Register your models here.


class ColorInline(admin.TabularInline):
    model = models.ProductColor


class ImageInline(admin.TabularInline):
    model = models.Image


class SpecInline(admin.TabularInline):
    model = models.Specification


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    model = models.Category
    search_fields = ['title']
    autocomplete_fields = ['parent']


class InStockFilter(admin.SimpleListFilter):
    title = 'In Stock'
    parameter_name = 'in_stock'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Yes'),
            ('0', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(product_colors__in_stock=True)
        if self.value() == '0':
            return queryset.filter(product_colors__in_stock=False)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    model = models.Product
    inlines = [ImageInline, SpecInline, ColorInline]
    search_fields = ['title']
    list_display = ['title', "price", "show_image", "check_in_stock", "slug", "get_colors"]
    list_filter = [InStockFilter]
    autocomplete_fields = ['category']

    def check_in_stock(self, obj):
        return obj.product_colors.filter(in_stock=True).exists()

    def get_colors(self, obj):
        items = obj.product_colors.all()
        colors = []
        for item in items:
            colors.append(item.color)
        return colors

    get_colors.short_description = "color"
    check_in_stock.short_description = "in stock"


admin.site.register(models.Color)
admin.site.register(models.Comment)
admin.site.register(models.Brand)
admin.site.register(models.Ip)
admin.site.register(models.Like)
