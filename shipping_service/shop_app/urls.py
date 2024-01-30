from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
from orders.handler import money_refund, deliver_order, order_cancellation, take_order, my_webhook_handler

app_name = 'shop_app'

urlpatterns = [
    path('', ProductsHome.as_view(), name='shop_app'),
    path('contacts', ContactsHome.as_view(), name='contacts'),
    path('<slug>', ProductsHome.as_view(), name='shop_app'),
    path('city/<slug:city_slug>', post_city, name='city_slug'),
    path('category/<slug:cat_slug>/', ProductsCategory.as_view(), name='category'),
    path('product/<slug:post_slug>/', ShowProduct.as_view(), name='product'),
    path('processing/', OrderProcessing.as_view(), name='processing'),
    path('take_order/', take_order, name='take_order'),
    path('order_work/', OrderWork.as_view(), name='order_work'),
    path('cancel_order/<int:pk>/', CancelOrder.as_view(), name='cancel_order'),
    path('order_cancellation/', order_cancellation, name='order_cancellation'),
    path('finalize_order/<int:pk>/', FinalizeOrder.as_view(), name='finalize_order'),
    path('deliver_order/', deliver_order, name='deliver_order'),
    path('money_refund/', money_refund, name='money_refund'),
    path('completed_orders/', CompletedOrders.as_view(), name='completed_orders'),
    path('returned_orders/', ReturnedOrders.as_view(), name='returned_orders'),
    path('return_order/<int:pk>/', ReturnOrder.as_view(), name='return_order'),
    path('production_hall/', ProductionHall.as_view(), name='production_hall'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('webhook/', csrf_exempt(my_webhook_handler))
]
