from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from orders.handler import my_webhook_handler
from shop_app.views import page_not_found


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop_app.urls', namespace='shop_app')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('captcha/', include('captcha.urls')),
    # path("__debug__/", include("debug_toolbar.urls")),
    path('webhook/', csrf_exempt(my_webhook_handler))
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = page_not_found
