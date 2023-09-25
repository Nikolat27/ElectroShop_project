from django.db.models import Avg
from django.shortcuts import render
from django.views.generic import DetailView

from product_app.models import Product, Review


# Create your views here.


def home_page(request):
    recent_products_1 = Product.objects.filter(category__name="Laptop").order_by("-created_at")[:3]
    recent_products_2 = Product.objects.filter(category__name="Mobile").order_by("-created_at")[:3]

    return render(request, "home_app/index.html", context={'ra1': recent_products_1, "ra2": recent_products_2})
