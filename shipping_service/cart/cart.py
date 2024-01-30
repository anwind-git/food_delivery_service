"""
Модуль для управления корзиной в службе доставки еды.
"""
from decimal import Decimal
from django.conf import settings
from shop_app.models import Products
from cart.forms import CartAddProductForm
from shipping_service.settings import shipping_cost


class Cart:
    """
    Класс, представляющий корзину для службы доставки еды.
    """
    def __init__(self, request):
        """
        Метод инициализации корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Перебираем товары в корзине и получаем товары из базы данных.
        """
        product_ids = self.cart.keys()
        cart = self.cart.copy()

        for product in Products.objects.filter(id__in=product_ids):
            item = cart[str(product.id)]
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                       'update': True})
            yield item

    def __len__(self):
        """
        Считаем сколько товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """
        Метод добавления товар в корзину или обновляем его количества.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Метод сохранения товара в корзине
        """
        self.session.modified = True

    def remove(self, product):
        """
        Метод удаления товара из корзины
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        Метод получения общей стоимость товаров в корзине
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def price_with_delivery(self):
        """
        Метод получения общей стоимость товаров в корзине
        """
        total_price = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        total_price += shipping_cost
        return total_price

    def clear(self):
        """
        Метод очищения корзины от товаров
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
