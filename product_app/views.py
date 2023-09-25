from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.template.loader import render_to_string
from .forms import CommentForm
from .models import Product, Category, Like, Comment, Review, Information, Contact
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg


# Create your views here.


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    informations = Information.objects.filter(product=product)
    related_products = Product.objects.filter(category__name=product.category.first().name)[:3]
    review_form = CommentForm()
    average_rating = Review.objects.filter(product=product).aggregate(
        reviews=Avg("rating"))  # rating is the field in model

    if request.method == "POST":
        body = request.POST.get("body")
        parent_id = request.POST.get("parent_id")
        review = request.POST.get("rating")
        if body:
            Comment.objects.create(product=product, body=body, parent_id=parent_id, author=request.user)
        if review:
            try:
                review1 = Review.objects.get(product=product, author=request.user)
                if review1:
                    review1.delete()
                    Review.objects.create(product=product, author=request.user, rating=review)
            except:
                Review.objects.create(product=product, author=request.user, rating=review)
    return render(request, "product_app/product.html", context={"product": product, "rp": related_products,
                                                                "ar": average_rating, "review_form": review_form,
                                                                "informations": informations})


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_app/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.likes.filter(product__slug=self.object.slug,
                                                                                 user_id=self.request.user.id).exists():
            context["is_liked"] = True
        else:
            context["is_liked"] = False
        return context


def store_page(request):
    queryset = Product.objects.all().order_by('-created_at')
    page_number = request.GET.get("page", 1)
    paginator = Paginator(queryset, 1)
    object_list = paginator.get_page(page_number)
    categories = Category.objects.all()

    if request.method == "GET":
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        category = request.GET.getlist("category")
        if category:
            queryset = queryset.filter(category__name__in=category).distinct()
            page_number = request.GET.get("page")
            paginator = Paginator(queryset, 1)
            object_list = paginator.get_page(page_number)

        if min_price and max_price:
            queryset = queryset.filter(price__lte=max_price, price__gte=min_price).distinct()
            page_number = request.GET.get("page")
            paginator = Paginator(queryset, 1)
            object_list = paginator.get_page(page_number)

    return render(request, "product_app/store.html", context={"products": object_list, "categories": categories})


def search_page(request):
    search = request.GET.get('search')
    if not search:
        search = ''
    products = Product.objects.filter(title__icontains=search)
    page_number = request.GET.get("page")
    paginator = Paginator(products, 1)
    object_list = paginator.get_page(page_number)
    return render(request, "product_app/store.html", context={'products': object_list})


def like(request, slug, pk):
    try:
        like = Like.objects.get(product__slug=slug, user_id=request.user.id)
        like.delete()
        liked_products = Product.objects.filter(likes__user=request.user)

        return JsonResponse({"response": "unliked", "likedproducts": len(liked_products)})
    except:
        Like.objects.create(product_id=pk, user_id=request.user.id)
        liked_products = Product.objects.filter(likes__user=request.user)
        return JsonResponse({"response": "liked", "likedproducts": len(liked_products)})


def autocomplete(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(title__istartswith=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)
        return JsonResponse(titles, safe=False)
    return render(request, "includes/searchbar.html")


def ajax_add_review(request, pk):
    product = get_object_or_404(Product, id=pk)
    user = request.user
    body = request.POST['body']
    rating = request.POST.get('rating')
    review_form = CommentForm()
    average_rating = Review.objects.filter(product=product).aggregate(
        reviews=Avg("rating"))  # rating is the field in model
    try:
        parent_id = request.POST['parent_id']
    except:
        parent_id = None

    if rating:
        try:
            rating1 = Review.objects.get(product=product, author=request.user)
            if rating1:
                rating1.delete()
                Review.objects.create(product=product, author=request.user, rating=rating)
        except:
            Review.objects.create(product=product, author=request.user, rating=rating)
    else:
        rating = None

    if body:
        review = Comment.objects.create(author=user, parent_id=parent_id, product=product,
                                        body=body)  # Comment creation

    comment1 = render_to_string("core/async/comment-list.html", {"product": product, "review_form": review_form},
                                request)
    comment2 = render_to_string("core/async/review-list.html", {"ar": average_rating}, request)
    return JsonResponse({
        'bool': True,
        'comment_part1': comment1,
        'comment_part2': comment2,
    })


def filter_products(request):
    if request.method == "GET":
        category = Category.objects.all()
        categories = request.GET.getlist("category")
        products = Product.objects.all().order_by("-created_at").distinct()
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        if len(categories) > 0:
            products = Product.objects.filter(category__name__in=categories).order_by("-created_at").distinct()
        #           If we want to give a list to the filter we should use "__in" after the filter name
        if min_price and max_price:
            products = products.filter(price__lte=max_price, price__gte=min_price).order_by("-created_at").distinct()

        page_number = request.GET.get("page")
        paginator = Paginator(products, 1)

        object_list = paginator.get_page(page_number)
        # data = render_to_string("core/async/product-list.html", {"products": object_list})
        # return JsonResponse({"data": data, "bool": True})
        return render(request, "product_app/store.html", context={"products": object_list, "categories": category})
    return redirect("home_app:main")


def wishlist(request):
    products = Product.objects.filter(likes__user=request.user)
    return render(request, "product_app/wishlist.html", context={"wishlist_products": products})


def remove_wishlist(request, pk):
    product = Like.objects.get(product=pk)
    product.delete()

    liked_products = Product.objects.filter(likes__user=request.user)
    total_likes = len(liked_products)
    data = render_to_string("core/async/unlike-products.html", {"wishlist_products": liked_products})
    return JsonResponse({"bool": True, "data": data, "likedproducts": total_likes})


def contact_us(request):
    if request.method == "POST":
        user = request.user
        subject = request.POST.get("subject")
        massage = request.POST.get("body")

        ticket = Contact.objects.create(user=user, subject=subject, massage=massage)
        recently_tickets = Contact.objects.filter(user=user)
        print(recently_tickets)
        return render(request, "product_app/contact.html", context={"rt": recently_tickets, "ticket": ticket})

    return render(request, "product_app/contact.html")


def contact_us2(request):
    pass
