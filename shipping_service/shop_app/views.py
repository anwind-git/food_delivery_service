from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from recipes.models import *
from .utils import *


class BaseClassProduct(DataMixin, ListView):
    model = Products
    template_name = 'shop_app/index.html'
    context_object_name = 'products'


class ProductsHome(BaseClassProduct):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Магазин')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user_context = self.get_user_context()
        city_id = user_context['city']['city_id']
        return Products.objects.filter(cities=city_id, publication=True).exclude(id__in=self.get_cart())


class ProductsCategory(BaseClassProduct):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Категория - {str(MenuCategories.objects.get(slug=self.kwargs["cat_slug"]))}',
                                      cat_selected=self.kwargs['cat_slug'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user_context = self.get_user_context()
        city_id = user_context['city']['city_id']
        return Products.objects.filter(menu_categories__slug=self.kwargs['cat_slug'],
                                       cities=city_id, publication=True).exclude(id__in=self.get_cart())


class ShowProduct(DataMixin, DetailView):
    model = Products
    template_name = 'shop_app/product.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        context['ingredients'] = AddIngredientToRecipe.objects.filter(recipe_id=obj.recipe.id).prefetch_related('ingredient')
        context['recipe'] = Recipes.objects.filter(id=obj.recipe.id).first()
        shelf_life_id = obj.shelf_life
        context['shelf_life'] = dict(Products.SHELF_LIFE)[shelf_life_id]
        c_def = self.get_user_context(title=context['product'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user_context = self.get_user_context()
        city_id = user_context['city']['city_id']
        return Products.objects.filter(cities=city_id, publication=True)


def city_slug(request, city_slug):
    request.session.pop('cart', None)
    city = Cities.objects.get(slug=city_slug)
    values = {'city_id': city.id, 'city_name': city.city, 'city_slug': city.slug}
    request.session['city'] = values
    return redirect('shop_app:shop_app')


class ContactsHome(DataMixin, ListView):
    model = NewManager
    template_name = 'shop_app/contacts.html'
    context_object_name = 'contacts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Контактная информация')
        return dict(list(context.items()) + list(c_def.items()))