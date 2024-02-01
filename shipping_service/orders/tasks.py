"""
Определяет задачи Celery для обработки заказов.
"""
import telebot
from django.conf import settings
from telebot import TeleBot
from celery import shared_task
from .models import Orders, OrderItem
from organization.models import DeliveryService
from shop_app.models import Products
from yookassa import Payment
from django.core import serializers
import logging

logger = logging.getLogger(__name__)

bot = TeleBot(settings.TOKEN_BOT)


@shared_task
def payment_search(payment_id):
    """
    Задача Celery для обновления статуса «оплачено» заказа на основе payment_id.
    """
    order = Orders.objects.get(identifier=payment_id)
    order.paid = True
    order.save()


@shared_task
def remove_buttons(chat_id, order_identifier, message_id):
    """
    Задача Celery отмена задачи для сотрудника службы доставки который не ответил на сообщении в заданный
    промежуток времени.
    """
    try:
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
        bot.send_message(chat_id, "Время вышло. Заказ предложен другому сотруднику службы доставки.")
        delivery_employee = DeliveryService.objects.get(status=True, telegram=chat_id)
        order = Orders.objects.get(identifier=order_identifier)
        order.delivery_service = None
        delivery_employee.status = False
        delivery_employee.save()
        order.save()
    except telebot.apihelper.ApiTelegramException as e:
        logger.exception(f'Задача Celery отмена задачи для сотрудника службы доставки: {e}')


@shared_task
def delivery_employee_refusal(chat_id, order_id):
    """
    Задача Celery для отмены заказа сотрудником службы доставки если он неготов выполнить его.
    """
    delivery_employee = DeliveryService.objects.get(status=True, telegram=chat_id)
    order = Orders.objects.get(id=order_id)
    delivery_employee.status = False
    order.delivery_service = None
    delivery_employee.save()
    order.save()


@shared_task
def delivery_confirmed(order_id, chat_id):
    """
    Задача Celery если сотрудник службы доставки успешно выполнил заказ.
    """
    order = Orders.objects.get(id=order_id)
    try:
        Payment.capture(order.identifier)
    except Exception as e:
        logger.exception(f'Задача Celery если сотрудник службы доставки успешно выполнил заказ: {e}')
    order.delivered = True
    order.save()

    delivery_service = DeliveryService.objects.get(telegram=chat_id)
    delivery_service.status = False
    delivery_service.save()


@shared_task
def customer_backed_out(order_id):
    """
    Задача Celery если клиент отказался от заказа, переводим статус заказа в не "оплачен".
    """
    order = Orders.objects.get(id=order_id)
    order.paid = False
    order.delivered = True
    order.save()


@shared_task
def add_new_order(identifier, city_json, address, email, phone, cart_list):
    """
    Задача Celery добавление нового заказа c его составом.
    """
    deserialized_city = serializers.deserialize('json', city_json, ignorenonexistent=True)
    city_instance = next(deserialized_city).object

    order = Orders(identifier=identifier, city=city_instance, phone=phone, email=email, address=address)
    order.save()

    product_ids = [item['product'] for item in cart_list]
    products = Products.objects.in_bulk(product_ids)

    order_items = []
    for item in cart_list:
        product = products[item['product']]
        order_items.append(OrderItem(
            order=order,
            product=product,
            price=item['price'],
            quantity=item['quantity']
        ))
    OrderItem.objects.bulk_create(order_items)

