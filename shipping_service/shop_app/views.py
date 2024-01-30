"""
Включает представления страниц магазина.
"""
from datetime import timedelta
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from recipes.models import Recipes, AddIngredientToRecipe
from organization.models import NewManager, Cities, DeliveryService
from shop_app.models import Products, MenuCategories
from .forms import LoginUserForm, Calendar, DenialService
from .utils import DataMixin
from orders.models import Orders, OrderItem
from django.db.models import Prefetch
from organization.models import UserProfile


class BaseClassProduct(DataMixin, ListView):
    """
    Базовый класс для представлений связанных с продукцией.
    """
    model = Products
    template_name = 'shop_app/index.html'
    context_object_name = 'products'


class ProductsHome(BaseClassProduct):
    """
    Вид для отображения товаров на главной странице.
    """

    def get_context_data(self, **kwargs):
        """
        Добавляет пользовательские контекстные данные для главной страницы.
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Магазин')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """
        Получите набор queryset для отображения товаров на главной странице.
        """
        user_context = self.get_user_context()
        city_id = user_context['city']['city_id']
        return Products.objects.filter(cities=city_id,
                                       publication=True).exclude(id__in=self.get_cart())


class ProductsCategory(BaseClassProduct):
    """
    Вид для отображения товаров в определенной категории.
    """

    def get_context_data(self, **kwargs):
        """
        Добавьте пользовательские контекстные данные для определенной категории товаров.
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=f'Категория - {str(MenuCategories.objects.get(slug=self.kwargs["cat_slug"]))}',
            cat_selected=self.kwargs['cat_slug'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """
        Получите набор запросов для отображения товаров в определенной категории.
        """
        user_context = self.get_user_context()
        city_id = user_context['city']['city_id']
        return Products.objects.filter(menu_categories__slug=self.kwargs['cat_slug'],
                                       cities=city_id,
                                       publication=True).exclude(id__in=self.get_cart())


class ShowProduct(DataMixin, DetailView):
    """
    Вид для отображения подробной информации о конкретном продукте.
    """
    model = Products
    template_name = 'shop_app/product.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """
        Добавьте пользовательские контекстные данные для отображения информации о продукте.
        """
        context = super().get_context_data(**kwargs)
        obj = self.object
        context['ingredients'] = (
            AddIngredientToRecipe.objects.filter(recipe_id=obj.recipe.id).prefetch_related('ingredient'))
        context['recipe'] = Recipes.objects.filter(id=obj.recipe.id).first()
        shelf_life_id = obj.shelf_life
        context['shelf_life'] = dict(Products.SHELF_LIFE)[shelf_life_id]
        c_def = self.get_user_context(title=context['product'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """
        Набор данных для отображения подробностей о конкретном продукте.
        """
        user_context = self.get_user_context()
        city_id = user_context['city']['city_id']
        return Products.objects.filter(cities=city_id, publication=True)


class ContactsHome(DataMixin, ListView):
    """
    Вид для отображения контактной информации магазина.
    """
    model = NewManager
    template_name = 'shop_app/contacts.html'
    context_object_name = 'contacts'

    def get_context_data(self, **kwargs):
        """
        Добавьте пользовательские контекстные данные для страницы с контактной информацией.
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Контактная информация')
        return dict(list(context.items()) + list(c_def.items()))


#################################################################################


class BaseClassOrders(LoginRequiredMixin, DataMixin, ListView):
    model = Orders
    context_object_name = 'processing'
    login_url = '/login/'


class OrderProcessing(BaseClassOrders):
    """
    Представление страницы вновь поступивших необработанных заказов в магазин.
    """
    template_name = 'shop_app/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Новые заказы')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Orders.objects.filter(paid=True, city__id=self.request.user.city.id, user__isnull=True, work=False,
                                     delivered=False).select_related('city').prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.filter(order_id__isnull=False))).order_by('id')


class OrderWork(BaseClassOrders):
    """
    Представление страницы принятых заказов рестораном.
    """
    template_name = 'shop_app/order_work.html'

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
                                     queryset=OrderItem.objects.filter(order_id__isnull=False))).order_by('id')


class CompletedOrders(BaseClassOrders):
    """
    Представление для страницы завершенных заказов.
    """
    template_name = 'shop_app/completed_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Завершенные')
        context['calendar_form'] = Calendar
        delivery_service_city = self.request.user.city
        context['available_employees'] = DeliveryService.objects.filter(status=False, work_authorization=True,
                                                                        city=delivery_service_city)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        calendar_form = Calendar(self.request.GET)
        user_id = self.request.user.id
        if calendar_form.is_valid():
            start_date = calendar_form.cleaned_data.get('my_date_field')

            if start_date:
                end_date = start_date + timedelta(days=1)

                return (Orders.objects.filter(paid=True, user__isnull=False, user=user_id,
                                              created__range=(start_date, end_date), work=False).prefetch_related(
                    Prefetch('items', queryset=OrderItem.objects.filter(order_id__isnull=False))))

        return Orders.objects.filter(paid=True, work=False, user__isnull=False, user=user_id).prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.filter(order_id__isnull=False))
        )


class ProductionHall(BaseClassOrders):
    """
    Представление для страницы производственного зала.
    """
    template_name = 'shop_app/production_hall.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Производственный зал')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user_id = self.request.user.id
        return Orders.objects.filter(paid=True, work=True, user=user_id).prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.filter(order_id__isnull=False))
        ).order_by('id')


class ReturnedOrders(BaseClassOrders):
    """
    Представление для страницы возвращенных заказов.
    """
    template_name = 'shop_app/returned_orders.html'

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
                                              created__range=(start_date, end_date)).prefetch_related(
                    Prefetch('items', queryset=OrderItem.objects.filter(order_id__isnull=False))))

        return Orders.objects.filter(paid=False, user=user_id).prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.filter(order_id__isnull=False))
        )


class BaseDetailOrder(LoginRequiredMixin, DataMixin, DetailView):
    model = Orders
    context_object_name = 'order'
    login_url = '/login/'


class CancelOrder(BaseDetailOrder):
    """
    Представление для страницы отмены заказа.
    """
    template_name = 'shop_app/cancel_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Отмена заказа')
        context['denial_service'] = DenialService
        return dict(list(context.items()) + list(c_def.items()))


class FinalizeOrder(BaseDetailOrder):
    """
    Представление для страницы завершения заказа.
    """
    template_name = 'shop_app/finalize_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Отправка заказа в доставку')
        return dict(list(context.items()) + list(c_def.items()))


class ReturnOrder(BaseDetailOrder):
    """
    Представление для страницы возврата денежных средств клиенту.
    """
    template_name = 'shop_app/return_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Возврат денежных средств клиенту')
        context['denial_service'] = DenialService
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    """
    Представление страницы авторизации пользователем.
    """
    form_class = LoginUserForm
    template_name = 'shop_app/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация пользователя'
        return context

    def get_success_url(self):
        return reverse_lazy('shop_app:processing')


def post_city(request, city_slug):
    """
    Установит выбранный город в сессии и перенаправит на главную страницу магазина. Очищает корзину.
    """
    request.session.pop('cart', None)
    city = Cities.objects.get(slug=city_slug)
    values = {'city_id': city.id, 'city_name': city.city, 'city_slug': city.slug}
    request.session['city'] = values
    return redirect('shop_app:shop_app')


def logout_user(request):
    logout(request)
    return redirect('shop_app:shop_app')
