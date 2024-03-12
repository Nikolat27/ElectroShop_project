from django import template
from product_app.models import Product

register = template.Library()


def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(",")[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@register.filter
def is_liked(request, pk):
    product = Product.objects.get(id=pk)
    user_ip = get_ip(request)
    if product.likes.filter(ip=user_ip).exists():
        return True
    else:
        return False
