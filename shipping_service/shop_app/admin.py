from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Products, MenuCategories


@admin.register(Products)
class ProductstAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'get_html_photo', 'price', 'time_update', 'queue', 'publication']
    search_fields = ['product_name', 'description', 'price']
    list_per_page = 15
    list_filter = ['menu_categories', 'publication', 'time_create', 'shelf_life']
    filter_horizontal = ['menu_categories', 'cities']
    fields = ['product_name', 'slug', 'description', 'image', 'get_html_photo', 'recipe',
              'shelf_life', 'price', 'cities', 'menu_categories', 'time_create', 'time_update', 'publication']
    readonly_fields = ['get_html_photo', 'time_create', 'time_update']
    list_editable = ['publication']
    prepopulated_fields = {'slug': ('product_name',)}

    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src={obj.image.url} width=50>")

    get_html_photo.short_description = "Миниатюра"


@admin.register(MenuCategories)
class MenuCategoriesAdmin(admin.ModelAdmin):
    list_display = ['categorie', 'slug', 'queue']
    list_per_page = 15
    prepopulated_fields = {'slug': ('categorie',)}


