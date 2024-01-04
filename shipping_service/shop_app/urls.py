from django.urls import path
from .views import *

app_name = 'shop_app'

urlpatterns = [
    path('', ProductsHome.as_view(), name='shop_app'),
    path('contacts', ContactsHome.as_view(), name='contacts'),
    path('<slug>', ProductsHome.as_view(), name='shop_app'),
    path('city/<slug:city_slug>', post_city, name='city_slug'),
    path('category/<slug:cat_slug>/', ProductsCategory.as_view(), name='category'),
    path('product/<slug:post_slug>/', ShowProduct.as_view(), name='product')
]