from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('new_order/', AddOrder.as_view(), name='new_order'),
]
