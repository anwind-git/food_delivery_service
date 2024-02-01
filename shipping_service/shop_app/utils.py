"""
Дополнительные функции приложения магазина.
"""
from django.db.models import Count
from organization.models import Cities, Addresses
from cart.forms import CartAddProductForm
from .models import MenuCategories
from django.core.cache import cache
from django.conf import settings

menu = [{'title': 'Магазин', 'url_name': '.'},
        {'title': 'Контакты', 'url_name': 'contacts'}
        ]


class DataMixin:
    """
    Класс Mixin, предоставляющий дополнительные данные для представлений.
    """
    paginate_by = 6

    def get_cart(self):
        """
        Метод получения идентификаторов товаров в корзине из сессии
        """
        product_ids_in_cart = map(str, self.request.session.get('cart', {}).keys())
        return product_ids_in_cart

    def get_user_context(self, **kwargs):
        """
        Метод получение контекстных данных, связанных с пользователем.
        """
        context = kwargs
        categories = cache.get('categories')
        if not categories:
            categories = MenuCategories.objects.annotate(Count('products')).order_by('queue')
            cache.set('categories', categories, settings.CACHE_TIME)
        if 'city' not in self.request.session:
            first_city = Cities.objects.first()
            values = {'city_id': first_city.id, 'city_name': first_city.city}
            self.request.session['city'] = values
        context['city'] = self.request.session['city']
        context['menu'] = menu
        context['categories'] = categories
        context['addresses'] = Addresses.objects.all()
        context['cart_product_form'] = CartAddProductForm
        city = cache.get('city')
        if not city:
            city = Cities.objects.all()
            cache.set('city', city, settings.CACHE_TIME)
        context['cities'] = city
        context['shipping_cost'] = settings.SHIPPING_COST
        context['SHOP_CURRENCY'] = settings.SHOP_CURRENCY
        context['single_telephone_number'] = settings.SINGLE_TELEPHONE_NUMBER
        context['site_name'] = settings.SITE_NAME
        if 'cat_select' not in context:
            context['cat_select'] = 0
        return context
