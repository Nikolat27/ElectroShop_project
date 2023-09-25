from django.contrib import admin
from . import models
# Register your models here.


class InformationAdmin(admin.StackedInline):
    model = models.Information


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "show_image")
    inlines = (InformationAdmin,)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    prepopulated_fields = {'slug': ("name",)}


admin.site.register(models.Color)
admin.site.register(models.Size)
admin.site.register(models.Information)
admin.site.register(models.Like)
admin.site.register(models.Comment)
admin.site.register(models.Review)
admin.site.register(models.Contact)
