from django.contrib import admin
from .models import Orders, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'id', 'city', 'phone', 'paid', 'created', 'updated', 'user', 'delivery_service']
    list_filter = ['city', 'paid', 'delivered', 'delivery_service', 'user', 'work', 'created']
    search_fields = ['phone', 'phone']
    list_per_page = 15
    inlines = [OrderItemInline]
