"""
Включает представления для страницы оформления заказа.
"""
import uuid
from django.shortcuts import redirect
from django.views.generic import TemplateView
from cart.cart import Cart
from shop_app.utils import DataMixin, OrderCreateForm, Cities
from dadata import Dadata
from yookassa import Configuration, Payment
from orders.api import toktoken_id, secret_dadata, account_id, secret_key_y
from .models import OrderItem, Orders
from django.http import HttpResponse

TOKEN = toktoken_id
SECRET = secret_dadata
dadata = Dadata(TOKEN, SECRET)

Configuration.account_id = account_id
Configuration.secret_key = secret_key_y


class YooMoneyCheckoutWidget(DataMixin, TemplateView):
    """
    Класс для формирования платежа для ЮKassa
    """
    template_name = 'orders/create.html'

    def get_context_data(self, **kwargs):
        """
        Добавляет пользовательские контекстные данные для страницы оформления заказа.
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Оформление заказа')
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request):
        """
        Метод формирует заказ и отправляет его в ЮKassa.
        """
        cart = Cart(request)
        if request.method == 'POST':
            try:
                last_object = Orders.objects.latest('id')
                last_id = last_object.id
                next_id = last_id + 1
            except Orders.DoesNotExist:
                next_id = 1

            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)

                items_list = []
                total_cost = 0

                for item in cart:
                    total_cost += item['price'] * item['quantity']

                    items_list.append({
                        "description": item['product'],
                        "quantity": item['quantity'],
                        "amount": {"value": item['price'], "currency": "RUB"},
                        "vat_code": "4",
                        "payment_mode": "full_prepayment",
                        "payment_subject": "commodity",
                        "country_of_origin_code": "RU",
                        "mark_mode": '0',
                        "mark_code_info": {"gs_1m": "DFGwNDY0MDE1Mzg2NDQ5MjIxNW9vY2tOelDFuUFwJh05MUVFMDYdOTJXK2ZaMy9uTjMvcVdHYzBjSVR3NFNOMWg1U2ZLV0dRMWhHL0UrZi8ydkDvPQ=="},
                        "measure": "piece"
                    })

                idempotence_key = str(uuid.uuid4())
                response = Payment.create({
                    "amount": {"value": total_cost, "currency": "RUB"},
                    "confirmation": {
                        "type": "redirect",
                        "return_url": f"https://{self.request.get_host()}"
                    },
                    "capture": True,
                    "description": f"Заказ №{next_id}",
                    "metadata": {'orderNumber': next_id},
                    "receipt": {"customer": {"email": self.request.POST.get("email")}, "items": items_list},
                    "payment_method_data": {"type": "bank_card"},
                }, idempotence_key)

                order.identifier = response.id
                order.phone = self.request.POST.get("phone")
                order.city = Cities.objects.get(id=self.get_user_context()['city']['city_id'])
                order.save()

                for item in cart:
                    OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                             quantity=item['quantity'])

                cart.clear()
                return redirect(response.confirmation.confirmation_url)
            else:
                return HttpResponse('Форма заполнена некорректно')
