from celery import shared_task
from django.shortcuts import get_object_or_404
from .models import Cities
from .models import DeliveryService


@shared_task
def add_employee(user_data):
    """
    Задача Celery для добавления нового сотрудника службы доставки.
    """
    city_instance = get_object_or_404(Cities, city=user_data['city'])

    delivery_service = DeliveryService.objects.create(
        fio=user_data['fio'],
        age=user_data['age'],
        phone=user_data['phone'],
        telegram=user_data['chat_id'],
        city=city_instance
    )
    delivery_service.save()

