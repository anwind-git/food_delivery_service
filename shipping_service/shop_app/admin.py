from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Products, MenuCategories


# регистрация модели товаров
@admin.register(Products)
class ProductstAdmin(admin.ModelAdmin):
    # Задает поля, которые будут отображаться в представлении списка интерфейса администратора модели Products.
    list_display = ['product_name', 'get_html_photo', 'price', 'time_update', 'queue', 'publication']
    # добавит поле поиска и позволит искать введенную информация по указанным полям.
    search_fields = ['product_name', 'description', 'price']
    # параметр указывает сколько товарав в интерфейсе администратора бедет отображаться на одной странице.
    list_per_page = 15
    # параметр указывает по каким полям организовать фильтрацию товаров.
    list_filter = ['menu_categories', 'publication', 'time_create', 'shelf_life']
    # указанные поля (многие ко многим) будут отабражены горизонтально.
    filter_horizontal = ['menu_categories', 'cities']
    # указывает, какие поля должны отображаться при просмотре или редактировании экземпляра модели.
    fields = ['product_name', 'slug', 'description', 'image', 'get_html_photo', 'recipe',
              'shelf_life', 'price', 'cities', 'menu_categories', 'time_create', 'time_update', 'publication']
    # поля которые будут отображаться только для чтения.
    readonly_fields = ['get_html_photo', 'time_create', 'time_update']
    # поля могут быть отредактированы непосредственно из списка интерфейса.
    list_editable = ['publication']
    # используется для автоматического заполнения значения поля на основе значения одного или нескольких других полей
    prepopulated_fields = {'slug': ('product_name',)}

    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src={obj.image.url} width=50>")

    get_html_photo.short_description = "Миниатюра"


# регистрация модели категорий меню для товаров
@admin.register(MenuCategories)
class MenuCategoriesAdmin(admin.ModelAdmin):
    list_display = ['categorie', 'slug', 'queue']
    list_per_page = 15
    prepopulated_fields = {'slug': ('categorie',)}
