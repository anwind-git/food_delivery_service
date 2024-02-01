from django.contrib import admin
from .models import NewManager, Addresses, Cities, UserProfile, DeliveryService


@admin.register(NewManager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['INN', 'last_name', 'first_name', 'middle_name', 'phone']


@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    list_display = ['city', 'addresse', 'phone', 'working_time']


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ['city']
    prepopulated_fields = {'slug': ('city',)}


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'first_name', 'city', 'address', 'phone', 'email']
    list_filter = ['city']
    search_fields = ['last_name', 'first_name', 'username', 'phone']


@admin.register(DeliveryService)
class DeliveryServiceAdmin(admin.ModelAdmin):
    list_display = ['city', 'fio', 'phone', 'telegram', 'status', 'day_off', 'work_authorization']
    search_fields = ['fio', 'telegram', 'phone']
    list_filter = ['city', 'status', 'day_off', 'work_authorization']
    list_editable = ['status', 'work_authorization', 'day_off']
