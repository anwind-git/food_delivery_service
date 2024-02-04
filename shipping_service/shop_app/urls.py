from django.urls import path

from organization.views import ContactsHome
from .views import *
from django.views.decorators.csrf import csrf_exempt
from orders.handler import my_webhook_handler

app_name = 'shop_app'

urlpatterns = [
    path('', ProductsHome.as_view(), name='shop_app'),
    path('contacts', ContactsHome.as_view(), name='contacts'),
    path('<slug>', ProductsHome.as_view(), name='shop_app'),
    path('city/<slug:city_slug>', post_city, name='city_slug'),
    path('category/<slug:cat_slug>/', ProductsCategory.as_view(), name='category'),
    path('product/<slug:post_slug>/', ShowProduct.as_view(), name='product'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('webhook/', csrf_exempt(my_webhook_handler))
]
