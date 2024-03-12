from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from product_app.models import Product, Comment, Category, Brand, Ip


# Create your views here.


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, "product_app/product_detail.html", context={"product": product})


def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(",")[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_comment(request, pk):
    if request.method == "POST":
        author = request.user
        product = get_object_or_404(Product, id=pk)
        text = request.POST.get("text")
        rating = request.POST.get("rating")
        parent_id = request.POST.get("parent_id")
        if parent_id:
            Comment.objects.create(author=author, product=product, text=text, rating=rating, parent_id=parent_id)
            return redirect("product_app:product_detail", pk)
        else:
            Comment.objects.create(author=author, product=product, text=text, rating=rating)
            return redirect("product_app:product_detail", pk)


def store_page(request):
    categories = Category.objects.all().order_by("title")
    brands = Brand.objects.all().order_by("title")
    products = Product.objects.all()

    page_number = request.GET.get("page", 1)
    paginator = Paginator(products, 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "product_app/store.html",
                  context={"products": page_obj, "brands": brands, "categories": categories})


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    price_min = request.GET.get("minPrice")
    price_max = request.GET.get("maxPrice")
    sort = request.GET.get("sortBy")
    page_number = request.GET.get("page")
    # show = request.GET.get("show")
    print(page_number)

    products = Product.objects.all().distinct()
    if categories and len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if brands and len(brands) > 0:
        products = products.filter(brand__id__in=brands).distinct()

    if price_min and price_max:
        products = products.filter(price__gte=int(float(price_min)), price__lte=int(float(price_max)))

    if sort == "available":
        products = products.filter(in_stock=True).order_by("-created_at").distinct()

    elif sort == "new":
        products = products.order_by("-created_at").distinct()

    elif sort == "popular":
        products = products.order_by("rate").distinct()

    elif sort == "discounted":
        products = products.filter(discount=True).order_by("-created_at").distinct()

    paginator = Paginator(products, 1)
    products = paginator.get_page(page_number)
    # if int(show) == 2:
    #     products = products[:2]
    # elif int(show) == 4:
    #     products = products[:4]
    # else:
    #     print("no show!")

    data = render_to_string('ajax_templates/store_ajax.html', {'products': products})

    return JsonResponse({"bool": True, 'data': data})


def add_like(request, pk):
    user_ip = get_ip(request)
    product = Product.objects.get(id=pk)
    ip_check = Ip.objects.filter(ip=user_ip).exists()

    print(f"{user_ip} - {product.title} - {ip_check}")

    if ip_check is False:
        Ip.objects.create(ip=user_ip)
        ip = Ip.objects.get(ip=user_ip)
        product.likes.add(ip)
        print("ip didnt exists but we added it")
        return JsonResponse({"response": "liked"})
    else:
        product_check = product.likes.filter(ip=user_ip).exists()
        if product_check is True:
            ip = Ip.objects.get(ip=user_ip)
            product.likes.remove(ip)
            print("unliked")
            return JsonResponse({"response": "unliked"})
        else:

            ip = Ip.objects.get(ip=user_ip)
            product.likes.add(ip)
            print("liked")
            return JsonResponse({"response": "liked"})
