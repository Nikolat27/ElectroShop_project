from celery import shared_task
from django.utils import timezone


# celery -A ElectroShop_project beat --loglevel=info
# Noticeable = You have to run both celery beat and celery command to run the periodic tasks!
@shared_task
def delete_order_automatically():
    from cart_app.models import Order
    current_time = timezone.now()
    x = current_time - timezone.timedelta(seconds=60)
    outdated_orders = Order.objects.filter(created_at__lt=x)
    outdated_orders.delete()
    return None


@shared_task
def delete_reservation_automatically(reserve_id):
    from .models import Reserve
    reserve = Reserve.objects.get(id=reserve_id)
    current_time = timezone.now()
    creation_time = reserve.created_at
    time_difference = current_time - creation_time
    time_difference = time_difference.total_seconds() / 60  # Convert to minutes
    if time_difference > 1:
        reserve.delete()
