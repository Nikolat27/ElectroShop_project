from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from product_app.models import Product, Comment, Category, Brand, Like


# Create your views here.


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    related_products = Product.objects.filter(category__in=product.category.all()).order_by("-id").distinct()
    return render(request, "product_app/product_detail.html",
                  context={"product": product, "related_products": related_products})


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
    products = Product.objects.all().order_by("-id")
    total = Product.objects.count()
    page_number = request.GET.get("page", 1)
    q = request.GET.get("q")

    # To Get the GET method parameters
    query_params = request.GET.copy()

    shownumber_options = ["1", "2"]
    sortby_options = ["Available", "New", "Popular", "Discounted"]

    if q and len(q):
        products = Product.objects.filter(title__icontains=q).order_by("-id").distinct()

    max_price = Product.objects.all().aggregate(Max('price'))['price__max']
    min_price = Product.objects.all().aggregate(Min('price'))['price__min']

    paginator = Paginator(products, 1)
    products = paginator.get_page(page_number)

    return render(request, "product_app/store.html",
                  context={"products": products, "brands": brands, "categories": categories, "total": total,
                           "sortBy_options": sortby_options,
                           "showNumber_options": shownumber_options, "query_params": query_params.urlencode(),
                           "max_price": max_price, "min_price": min_price})


def filter_data(request):
    # Getting Get parameters
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    price_min = request.GET.get("minPrice")
    price_max = request.GET.get("maxPrice")
    sort = request.GET.get("sortBy")
    show = request.GET.get('show', 1)
    q = request.GET.get("q")
    page_number = request.GET.get("page", 1)
    products = Product.objects.all().distinct()

    # To Get the GET method parameters
    query_params = request.GET.copy()

    # To Avoid many 'page' parameters
    if "page" in query_params:
        del query_params["page"]

    # If user has searched sth
    if q and len(q) > 0:
        products = products.filter(title__icontains=q).order_by("-id").distinct()

    # Start Filtering
    if categories and len(categories) > 0:
        products = products.filter(category__id__in=categories).order_by("-id").distinct()

    if brands and len(brands) > 0:
        products = products.filter(brand__id__in=brands).distinct()

    if price_min and price_max:
        products = products.filter(price__gte=int(float(price_min)), price__lte=int(float(price_max)))

    # Start Sorting
    if sort == "available":
        products = products.filter(in_stock=True).order_by("-id").distinct()
    elif sort == "new":
        products = products.order_by("-created_at").distinct()
    elif sort == "popular":
        products = Product.objects.annotate(avg_rating=Avg('comments__rating')).order_by('-avg_rating')
    elif sort == "discounted":
        products = products.filter(discount=True).order_by("-created_at").distinct()

    # How many products in each Page
    if show and int(show) == 2:
        paginator = Paginator(products, 2)
    else:
        paginator = Paginator(products, 1)

    products = paginator.get_page(page_number)

    # Ajax templates for rendering
    data = render_to_string('ajax_templates/store_ajax.html', {'products': products})
    data2 = render_to_string("ajax_templates/pagination_ajax.html",
                             {"products": products, "query_params": query_params.urlencode()})
    return JsonResponse({"bool": True, 'data': data, "data2": data2})


def add_like(request, pk):
    product = Product.objects.get(id=pk)
    if request.user.is_authenticated:
        user = request.user
        user_check = Like.objects.filter(product=product, user=user).exists()
        if user_check:
            like = Like.objects.get(product=product, user=user)
            like.delete()
            total = Like.objects.filter(product_id=pk).aggregate(total=Count('id'))['total']
            return JsonResponse({"response": "unliked", "total": total})
        else:
            Like.objects.create(product=product, user=user)
            total = Like.objects.filter(product_id=pk).aggregate(total=Count('id'))['total']
            return JsonResponse({"response": "liked", "total": total})
    else:
        return JsonResponse({"response": "anonymous"})
    # else:
    #     user_ip = get_ip(request)
    #     ip_check = Ip.objects.filter(ip=user_ip).exists()
    #     user_ip = get_ip(request)
    #     if ip_check is False:
    #         Ip.objects.create(ip=user_ip)
    #         ip = Ip.objects.get(ip=user_ip)
    #         product.likes.add(ip)
    #         total = product.likes.count()
    #         return JsonResponse({"response": "liked", "total": total})
    #     else:
    #         product_check = product.likes.filter(ip=user_ip).exists()
    #         if product_check is True:
    #             ip = Ip.objects.get(ip=user_ip)
    #             product.likes.remove(ip)
    #             total = product.likes.count()
    #             return JsonResponse({"response": "unliked", "total": total})
    #         else:
    #             ip = Ip.objects.get(ip=user_ip)
    #             product.likes.add(ip)
    #             total = product.likes.count()
    #             return JsonResponse({"response": "liked", "total": total})


@login_required
def wishlist_page(request):
    user = request.user
    liked_products = Like.objects.filter(user=user).values("product")

    products = Product.objects.filter(id__in=liked_products)
    return render(request, "product_app/wishlists.html", context={"products": products})


def autocomplete(request):
    if 'term' in request.GET:
        products = Product.objects.filter(title__istartswith=request.GET.get('term'))
        titles = []
        for product in products:
            titles.append(product.title)
        return JsonResponse(titles, safe=False)
    return render(request, "home_app/index.html")
