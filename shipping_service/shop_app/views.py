"""
Включает представления, связанные с магазином.
"""
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from recipes.models import Recipes, AddIngredientToRecipe
from organization.models import NewManager, Cities
from shop_app.models import Products, MenuCategories
from .utils import DataMixin


class BaseClassProduct(DataMixin, ListView):
    """
    Базовый класс для представлений, связанных с продукцией.
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
                                       cities=city_id, publication=True).exclude(id__in=self.get_cart())


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


def post_city(request, city_slug):
    """
    Установит выбранный город в сессии и перенаправит на главную страницу магазина. Очищает корзину.
    """
    request.session.pop('cart', None)
    city = Cities.objects.get(slug=city_slug)
    values = {'city_id': city.id, 'city_name': city.city, 'city_slug': city.slug}
    request.session['city'] = values
    return redirect('shop_app:shop_app')
