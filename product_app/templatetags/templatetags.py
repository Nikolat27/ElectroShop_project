from django import template
from django.db.models import Count

from product_app.models import Product, Like

register = template.Library()


def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(",")[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@register.filter
def is_liked(request, pk):  # Seeing that you have liked a product or No!
    user = request.user
    product = Product.objects.get(id=pk)
    is_liked = Like.objects.filter(product=product, user=user)
    if is_liked:
        return True
    else:
        return False


@register.filter
def wishlist_count(request):  # Total products you have been liked!
    if request.user.is_authenticated:
        user = request.user
        count = Like.objects.filter(user=user).aggregate(total=Count('id'))['total']
        return count
    else:
        return 0


@register.filter
def total_product_likes(pk):  # Total Likes for 1 Product
    total = Like.objects.filter(product_id=pk).aggregate(total=Count('id'))['total']
    return total


@register.filter
def get_list(dictionary, key):
    return dictionary.getlist(key)


@register.filter()
def as_string(value):
    return str(value)


@register.filter
def x(value):
    if value:
        return "request.GET.category[]"
    else:
        return False
