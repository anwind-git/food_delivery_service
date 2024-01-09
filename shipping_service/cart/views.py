"""
Определяет представления для приложения корзины.
"""
from django.views.generic import TemplateView
from shop_app.utils import DataMixin


class CartDetailView(DataMixin, TemplateView):
    """
    Класс для отображения деталей корзины.
    """
    template_name = 'cart/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Корзина')
        return dict(list(context.items()) + list(c_def.items()))
