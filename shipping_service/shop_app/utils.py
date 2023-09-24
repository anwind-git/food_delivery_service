from .models import *
from django.db.models import *
from organization.models import *


menu = [{'title': 'Магазин', 'url_name': '.'},
        {'title': 'Контакты', 'url_name': 'contacts'}
        ]


class DataMixin:
    paginate_by = 6

    def get_cart(self):
        product_ids_in_cart = map(str, self.request.session.get('cart', {}).keys())
        return product_ids_in_cart

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = MenuCategories.objects.annotate(Count('products')).order_by('queue')
        if 'city' not in self.request.session:
            first_city = Cities.objects.first()
            values = {'city_id': first_city.id, 'city_name': first_city.city}
            self.request.session['city'] = values
        context['city'] = self.request.session['city']
        context['menu'] = menu
        context['categories'] = categories
        context['addresses'] = Addresses.objects.all()
        context['cities'] = Cities.objects.all()
        if 'cat_select' not in context:
            context['cat_select'] = 0
        return context



