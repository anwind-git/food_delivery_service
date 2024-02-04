"""
Включает представления для страницы оформления заказа.
"""
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Max, Prefetch
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView
from cart.cart import Cart
from organization.models import Cities, DeliveryService
from shop_app.utils import DataMixin
from dadata import Dadata
from yookassa import Configuration, Payment
from .forms import OrderCreateForm, Calendar, DenialService
from .models import Orders, OrderItem
from .tasks import add_new_order

token = settings.TOKEN_ID_DADATA
secret = settings.SECRET_DADATA
dadata = Dadata(token, secret)

Configuration.account_id = settings.ACCOUNT_YOOKASSA
Configuration.secret_key = settings.SECRET_KEY_YOOKASSA


class AddOrder(DataMixin, FormView):
    form_class = OrderCreateForm
    template_name = 'orders/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Оформление заказа')
        context.update(c_def)
        return context

    def form_valid(self, form):
        cart = Cart(self.request)
        cart_list = []
        for cart_item in cart:
            product_id = cart_item['product'].id
            cart_list.append({
                'product': product_id,
                'price': cart_item['price'],
                'quantity': cart_item['quantity']
                })
        max_pk = Orders.objects.aggregate(Max('pk'))['pk__max']
        order_id = max_pk + 1 if max_pk else 1
        items_list = []
        city_id = self.get_user_context()['city']['city_id']
        city = Cities.objects.get(id=city_id)
        city_json = serializers.serialize('json', [city])
        address = self.request.POST.get("address")
        email = self.request.POST.get("email")
        phone = self.request.POST.get("phone")
        for item in cart:
            items_list.append({
                "description": item['product'],
                "quantity": item['quantity'],
                "amount": {"value": item['price'], "currency": settings.FIAT_CURRENCY},
                "tax_system_code": settings.TAX_SYSTEM_CODE,
                "vat_code": settings.VAT_CODE,
                "payment_mode": settings.PAYMENT_MODE,
                "payment_subject": settings.PAYMENT_SUBJECT,
                "country_of_origin_code": settings.COUNTRY_OF_ORIGIN_CODE,
                "measure": settings.MEASURE
            })
        items_list.append({
            "description": 'Доставка заказа',
            "quantity": 1,
            "amount": {"value": settings.SHIPPING_COST, "currency": settings.FIAT_CURRENCY},
            "tax_system_code": settings.TAX_SYSTEM_CODE,
            "vat_code": settings.VAT_CODE,
            "payment_mode": settings.PAYMENT_MODE,
            "payment_subject": 'service',
            "measure": settings.MEASURE
        })
        response = Payment.create({
            "amount": {"value": Cart.price_with_delivery(cart), "currency": settings.FIAT_CURRENCY},
            "payment_method_data": {"type": settings.METHOD_PAYMENT},
            "confirmation": {"type": "redirect", "return_url": f"https://{self.request.get_host()}"},
            "capture": False,
            "description": f"Заказ №{order_id} | поддержка: {settings.SINGLE_TELEPHONE_NUMBER}",
            "receipt": {"customer": {"email": email}, "items": items_list},
        }, uuid.uuid4())
        identifier = response.id
        add_new_order.delay(identifier, city_json, address, email, phone, cart_list)
        cart.clear()
        return redirect(response.confirmation.confirmation_url)


class BaseClassOrders(LoginRequiredMixin, DataMixin, ListView):
    model = Orders
    context_object_name = 'processing'
    login_url = '/login/'


class OrderProcessing(BaseClassOrders):
    """
    Представление страницы вновь поступивших необработанных заказов в магазин.
    """
    template_name = 'orders/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Новые заказы')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Orders.objects.filter(paid=True, city__id=self.request.user.city.id, user__isnull=True, work=False,
                                     delivered=False).prefetch_related(Prefetch('items',
                                     queryset=OrderItem.objects.filter(order__isnull=False).select_related(
                                                                                    'product'))).order_by('id')


class OrderWork(BaseClassOrders):
    """
    Представление страницы принятых заказов.
    """
    template_name = 'orders/order_work.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Заказы в работе')
        delivery_service_city = self.request.user.city
        context['available_employees'] = DeliveryService.objects.filter(status=False, work_authorization=True,
                                                                        city=delivery_service_city)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Orders.objects.filter(paid=True, user=self.request.user.id, work=True,
                                     delivered=False).select_related('city').prefetch_related(Prefetch('items',
                                                                                                       queryset=OrderItem.objects.filter(
                                                                                                           order__isnull=False).select_related(
                                                                                                           'product'))).order_by(
            'id')


class CompletedOrders(BaseClassOrders):
    """
    Представление для страницы завершенных заказов.
    """
    template_name = 'orders/completed_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Завершенные')
        context['calendar_form'] = Calendar
        delivery_service_city = self.request.user.city
        context['available_employees'] = DeliveryService.objects.filter(status=False, work_authorization=True,
                                                                        city=delivery_service_city).select_related(
            'city')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        calendar_form = Calendar(self.request.GET)
        user_id = self.request.user.id

        if calendar_form.is_valid():
            start_date = calendar_form.cleaned_data.get('my_date_field')

            if start_date:
                end_date = start_date + timedelta(days=1)

                return (Orders.objects.filter(paid=True, user=user_id, work=False,
                                              created__range=(start_date, end_date)).select_related(
                    'delivery_service').prefetch_related(
                    Prefetch('items',
                             queryset=OrderItem.objects.filter(order__isnull=False).select_related('product'))))

        return (Orders.objects.filter(
            paid=True, work=False,
            user=user_id).select_related('delivery_service')
                .prefetch_related(Prefetch('items', queryset=OrderItem.objects.filter(
            order__isnull=False).select_related('product'))))


class ProductionHall(BaseClassOrders):
    """
    Представление для страницы производственного зала.
    """
    template_name = 'orders/production_hall.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Производственный зал')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Orders.objects.filter(paid=True, work=True, user=self.request.user.id).prefetch_related(
            Prefetch('items',
                     queryset=OrderItem.objects.filter(order_id__isnull=False).select_related('product'))).order_by(
            'id')


class ReturnedOrders(BaseClassOrders):
    """
    Представление для страницы возвращенных заказов.
    """
    template_name = 'orders/returned_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Возвращенные')
        context['calendar_form'] = Calendar
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        calendar_form = Calendar(self.request.GET)
        user_id = self.request.user.id
        if calendar_form.is_valid():
            start_date = calendar_form.cleaned_data.get('my_date_field')

            if start_date:
                end_date = start_date + timedelta(days=1)

                return (Orders.objects.filter(paid=False, user=user_id,
                                              created__range=(start_date, end_date)).select_related('delivery_service'))

        return Orders.objects.filter(paid=False, user=user_id, work=False).select_related('delivery_service')


def order_ready_delivery(request):
    """
    Метод представления страницы готовности заказа к доставке.
    """
    if request.method == 'POST':
        order_identifier = request.POST.get("order_identifier")
        order = Orders.objects.get(identifier=order_identifier)
        context = {'order_id': order.id, 'order_identifier': order.identifier, 'order_phone': order.phone,
                   'denial_service': DenialService, 'order_address': order.address, 'order_created': order.created}
        return render(request, 'orders/order_ready_delivery.html', context)
    return redirect('orders:order_work')


def payment_acceptance(request):
    """
    Метод представления страницы приема оплаты за заказ.
    """
    if request.method == 'POST':
        order_identifier = request.POST.get("payment_identifier")
        order = Orders.objects.get(identifier=order_identifier)
        context = {'order_id': order.id, 'order_identifier': order.identifier, 'order_phone': order.phone,
                   'denial_service': DenialService, 'order_address': order.address, 'order_created': order.created}
        return render(request, 'orders/payment_acceptance.html', context)
    return redirect('orders:completed_orders')


def cancel_order(request):
    """
    Метод представления страницы отмены заказа.
    """
    if request.method == 'POST':
        order_identifier = request.POST.get("cancel_identifier")
        order = Orders.objects.get(identifier=order_identifier)
        context = {'order_id': order.id, 'order_identifier': order.identifier, 'order_phone': order.phone,
                   'denial_service': DenialService, 'order_address': order.address, 'order_created': order.created}
        return render(request, 'orders/cancel_order.html', context)
    return redirect('orders:completed_orders')


def order_status(request):
    """
    Метод представления страницы статуса платежа.
    """
    if request.method == 'POST':
        order_identifier = request.POST.get("identifier")
        context = {'result': Payment.find_one(order_identifier), 'identifier': order_identifier}
        return render(request, 'orders/order_status.html', context)
    return redirect('orders:completed_orders')
