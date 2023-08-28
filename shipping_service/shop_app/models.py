from django.urls import reverse
from django.db import models
from recipes.models import Recipes
from organization.models import Cities
from decimal import Decimal
import math


# класс товаров
class Products(models.Model):
    # выпадающий список для поля “Срок годности”
    SHELF_LIFE = (
        (0, '---------'),
        (1, '5 суток при температуре от +2 до +5 °C'),
        (2, '48 часов при температуре от +2 до +5 °C'),
        (2, '72 часа при температуре от +2 до +5 °C')
    )

    image = models.ImageField(upload_to='static/image/%Y/%m/%d/', verbose_name='Изображение')
    product_name = models.CharField(max_length=50, verbose_name='Наименование')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(verbose_name='Полное описание')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, verbose_name='Рецепт')
    shelf_life = models.IntegerField(choices=SHELF_LIFE, default=0, verbose_name='Срок годности')
    price = models.IntegerField(verbose_name='Цена')
    cities = models.ManyToManyField(Cities, verbose_name='Города обслуживания')
    menu_categories = models.ManyToManyField('MenuCategories', verbose_name='Категория блюда')
    queue = models.IntegerField(editable=False, default=0, verbose_name='Очередность')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    publication = models.BooleanField(default=True, verbose_name='Опубликовано')

    # метаданные для модели
    class Meta:
        db_table = 'products'
        verbose_name = 'блюда'
        verbose_name_plural = 'Продукция'
        # экземпляры будут упорядочены по полю в порядке возрастания
        ordering = ['id']

    # возвращает значение атрибута для каждого экземпляра модели
    def __str__(self):
        return self.product_name

    # метод возвращает URL-адрес представления "product" с ключевым словом "post_slug"
    def get_absolute_url(self):
        return reverse('product', kwargs={'post_slug': self.slug})

    # сразу прибавляет 3,7% к цене, комиссия за операцию в юкасса.
    def save(self, *args, **kwargs):
        self.price = math.ceil(self.price * Decimal(1 + 0.037))
        super().save(*args, **kwargs)


# класс категорий меню товаров
class MenuCategories(models.Model):
    categorie = models.CharField(max_length=20, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    queue = models.IntegerField(verbose_name='Очередность')

    class Meta:
        db_table = 'menu_categories'
        verbose_name = 'категорию '
        verbose_name_plural = 'Категории блюд'

    def __str__(self):
        return self.categorie

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
