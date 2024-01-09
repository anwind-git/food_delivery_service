"""
Определяет задачи Celery для обработки заказов.
"""
from celery import shared_task
from .models import Orders


@shared_task
def payment_search(payment_id):
    """
    Задача Celery для обновления статуса «оплачено» заказа на основе payment_id.
    """
    order = Orders.objects.filter(identifier=payment_id).first()
    order.paid = True
    order.save()
