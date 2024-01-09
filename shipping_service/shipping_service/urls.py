from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from shop_app.views import my_webhook_handler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop_app.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('orders.urls', namespace='orders')),
    path('webhook/', csrf_exempt(my_webhook_handler))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
