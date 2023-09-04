from django.contrib import admin
from .models import Manager, Addresses, Cities


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['INN', 'last_name', 'first_name', 'middle_name', 'phone']


@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    list_display = ['city', 'addresse']


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ['city']
    prepopulated_fields = {'slug': ('city',)}
