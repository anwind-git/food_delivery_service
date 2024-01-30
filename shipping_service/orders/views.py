"""
Включает представления для страницы оформления заказа.
"""
import uuid
from django.conf import settings
from django.core import serializers
from django.db.models import Max
from django.shortcuts import redirect
from django.views.generic import FormView
from cart.cart import Cart
from organization.models import Cities
from shop_app.utils import DataMixin
from dadata import Dadata
from yookassa import Configuration, Payment
from .forms import OrderCreateForm
from .models import Orders
from .tasks import add_new_order
from shipping_service.settings import (currency1, method_payment, vat_code, payment_mode, payment_subject,
                                       tax_system_code, country_of_origin_code, measure, single_telephone_number,
                                       shipping_cost)

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
                "amount": {"value": item['price'], "currency": currency1},
                "tax_system_code": tax_system_code,
                "vat_code": vat_code,
                "payment_mode": payment_mode,
                "payment_subject": payment_subject,
                "country_of_origin_code": country_of_origin_code,
                "measure": measure
            })
        items_list.append({
            "description": 'Доставка заказа',
            "quantity": 1,
            "amount": {"value": shipping_cost, "currency": currency1},
            "tax_system_code": tax_system_code,
            "vat_code": vat_code,
            "payment_mode": payment_mode,
            "payment_subject": 'service',
            "measure": measure
        })
        response = Payment.create({
            "amount": {"value": Cart.price_with_delivery(cart), "currency": currency1},
            "payment_method_data": {"type": method_payment},
            "confirmation": {"type": "redirect", "return_url": f"https://{self.request.get_host()}"},
            "capture": False,
            "description": f"Заказ №{order_id} | поддержка: {single_telephone_number}",
            "receipt": {"customer": {"email": email}, "items": items_list},
        }, uuid.uuid4())
        identifier = response.id
        add_new_order.delay(identifier, city_json, address, email, phone, cart_list)
        cart.clear()
        return redirect(response.confirmation.confirmation_url)
