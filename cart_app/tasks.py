from ElectroShop_project import settings
from celery import Celery, shared_task

from product_app.models import Comment


@shared_task
def delete_order_automatically():
    try:
        x = Comment.objects.get(id=1)
        x.delete()
        return None
    except:
        pass
