from django.urls import path

from .handler import take_order, order_cancellation, money_refund, deliver_order
from .views import *

app_name = 'orders'

urlpatterns = [
    path('new_order/', AddOrder.as_view(), name='new_order'),
    path('processing/', OrderProcessing.as_view(), name='processing'),
    path('take_order/', take_order, name='take_order'),
    path('order_work/', OrderWork.as_view(), name='order_work'),
    path('cancel_order/', cancel_order, name='cancel_order'),
    path('order_cancellation/', order_cancellation, name='order_cancellation'),
    path('order_ready_delivery/', order_ready_delivery, name='order_ready_delivery'),
    path('deliver_order/', deliver_order, name='deliver_order'),
    path('money_refund/', money_refund, name='money_refund'),
    path('completed_orders/', CompletedOrders.as_view(), name='completed_orders'),
    path('payment_acceptance/', payment_acceptance, name='payment_acceptance'),
    path('returned_orders/', ReturnedOrders.as_view(), name='returned_orders'),
    path('production_hall/', ProductionHall.as_view(), name='production_hall'),
    path('order_status/', order_status, name='order_status'),
]
