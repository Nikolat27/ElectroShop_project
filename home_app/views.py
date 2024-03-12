from django.shortcuts import render

from product_app.models import Product


# Create your views here.


def home_page(request):
    products = Product.objects.all().order_by("-created_at")[:3]
    return render(request, "home_app/index.html", context={"products": products})
