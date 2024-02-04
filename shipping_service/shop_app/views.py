"""
Включает представления страниц магазина.
"""
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from recipes.models import Recipes, AddIngredientToRecipe
from organization.models import Cities
from shop_app.models import Products, MenuCategories
from .forms import LoginUserForm
from .utils import DataMixin
from django.conf import settings
from .utils import menu


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
        context['ingredients'] = AddIngredientToRecipe.objects.filter(recipe_id=obj.recipe.id).prefetch_related('ingredient')
        context['recipe'] = Recipes.objects.filter(id=obj.recipe.id).first()
        shelf_life_id = obj.shelf_life
        context['shelf_life'] = dict(Products.SHELF_LIFE)[shelf_life_id]
        c_def = self.get_user_context(title=context['product'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """
        Проверяет опубликован или нет продукт, принадлежность к городу выбранному клиентом.
        """
        user_context = self.get_user_context()
        city_id = user_context['city']['city_id']
        return Products.objects.filter(cities=city_id, publication=True)


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
        return reverse_lazy('orders:processing')


def post_city(request, city_slug):
    """
    Метод устанавливает город в сессии. Очищает корзину.
    """
    request.session.pop('cart', None)
    city = Cities.objects.get(slug=city_slug)
    values = {'city_id': city.id, 'city_name': city.city, 'city_slug': city.slug}
    request.session['city'] = values
    return redirect('shop_app:shop_app')


def logout_user(request):
    """
    Метод выхода пользователя из панели управления.
    """
    logout(request)
    return redirect('shop_app:login')


def page_not_found(request, exception):
    context = {'site_name': settings.SITE_NAME}
    return render(request, 'shop_app/page_not_found.html', context)
