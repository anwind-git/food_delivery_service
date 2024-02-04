import random
import uuid
import json
import telebot
from django.conf import settings
from telebot import TeleBot
from django.shortcuts import redirect, get_object_or_404
from .models import DeliveryService, UserProfile
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .models import Orders
from .tasks import remove_buttons
from yookassa import Payment
from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification
from django.views.decorators.csrf import csrf_exempt
from .tasks import payment_search
import logging

logger = logging.getLogger(__name__)

bot = TeleBot(settings.TOKEN_BOT)


def take_order(request):
    """
    Метод приема нового заказа в обработку рестораном.
    """
    if request.method == 'POST':
        try:
            order_id = request.POST.get("order_id")
            user_id = request.POST.get("user_id")
            order = get_object_or_404(Orders, pk=order_id)
            user_id = get_object_or_404(UserProfile, pk=user_id)

            if not order.work:
                order.user = user_id
                order.work = True
                order.save()

                return redirect('orders:order_work')
            else:
                return redirect('orders:processing')
        except Exception as e:
            logger.exception(f'Ошибка в методе приема нового заказа: {e}')
    return redirect('orders:order_work')


def send_delivery_message(selected_employee, order_id):
    """
    Метод отправки сообщения сотруднику доставки, с предложением нового задания.
    """
    chat_id = selected_employee.telegram
    keyboard = InlineKeyboardMarkup()
    yes = InlineKeyboardButton("Да", callback_data='yes:' + str(order_id.id))
    no = InlineKeyboardButton("Нет", callback_data='no:' + str(order_id.id))
    keyboard.add(yes, no)

    try:
        message = bot.send_message(chat_id=chat_id, text=f"Для Вас есть Заказ №{order_id.id}:\n"
                                                         f"Забрать: {order_id.user.address}\n"
                                                         f"Доставить: {order_id.address}\n"
                                                         f"Контактный телефон клиента: {order_id.phone}\n\n"
                                                         f"{selected_employee.fio} Вы готовы выполнить этот заказ?\n",
                                   reply_markup=keyboard)

        selected_employee.status = True
        selected_employee.save()
        order_id.work = False
        order_id.delivery_service = selected_employee
        order_id.save()
        remove_buttons.apply_async(args=[chat_id, order_id.identifier,  message.message_id],
                                   countdown=settings.RESPONSE_TIME)
    except telebot.apihelper.ApiException as e:
        logger.info(f'Сотрудник службы доставки заблокировал бота')
        selected_employee.work_authorization = False
        selected_employee.save()


def choose_security_officer(order_id):
    """
    Метод рандомного подбора сотрудника службы доставки для выполнения заказа
    """
    available_employees = DeliveryService.objects.filter(city_id=order_id.city.id, work_authorization=True, status=False,
                                                         day_off=False)
    try:
        random_employee = random.choice(available_employees)
        send_delivery_message(random_employee, order_id)
    except IndexError:
        logger.info('Нет свободных сотрудников службы доставки')
        return redirect('order:order_work')


def deliver_order(request):
    """
    Метод получения данных заказа перед отправкой в службу доставки.
    """
    if request.method == 'POST':
        order_identifier = request.POST.get("order_identifier")
        order = Orders.objects.get(identifier=order_identifier)
        choose_security_officer(order)
    return redirect('orders:completed_orders')


def money_refund(request):
    """
    Метод получения данных для возврата средств заказчику.
    """
    if request.method == 'POST':
        order_identifier = request.POST.get("order_identifier")
        denial_service = request.POST.get("denial_service")
        employee_id = request.POST.get("employee_id")
        idempotence_key = str(uuid.uuid4())
        response = Payment.cancel(order_identifier, idempotence_key)

        order = Orders.objects.get(identifier=order_identifier)
        employee = DeliveryService.objects.get(id=employee_id)

        order.delivered = False
        order.denial_service = denial_service
        order.save()
        employee.status = False
        employee.save()
    return redirect('orders:returned_orders')


def order_cancellation(request):
    """
    Метод отмены заказа и возврата денежных средств клиенту.
    """
    if request.method == 'POST':
        idempotence_key = str(uuid.uuid4())
        order_identifier = request.POST.get("order_identifier")
        denial_service = request.POST.get("denial_service")
        order = Orders.objects.get(identifier=order_identifier)
        if order.delivery_service is not None:
            employee = DeliveryService.objects.get(id=order.delivery_service.id)
            employee.status = False
            employee.save()
        try:
            response = Payment.cancel(
                order.identifier,
                idempotence_key
            )
        except Exception as e:
            logger.exception(f'Ошибка в методе отмены заказа: {e}')
        order.paid = False
        order.work = False
        order.delivered = False
        order.denial_service = denial_service
        order.save()
    return redirect('orders:order_work')


@csrf_exempt
def my_webhook_handler(request):
    """
    Метод принимает HTTP-уведомления от Юкасса, о статусе платежа
    """
    try:
        event_json = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return HttpResponse(status=400)
    notification_object = WebhookNotification(event_json)
    payment = notification_object.object
    payment_log = Payment.find_one(payment.id)
    if payment_log.status == 'waiting_for_capture':
        payment_search.delay(payment.id)
        return HttpResponse(status=200)
    return HttpResponse(status=400)
