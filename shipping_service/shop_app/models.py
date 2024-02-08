"""
Модуль моделей Django в службе доставки еды.
"""

from decimal import Decimal
import math

from django.conf import settings
from django.urls import reverse
from django.db import models
from recipes.models import Recipes
from organization.models import Cities


class Products(models.Model):
    """
    Класс добавляет новый товар в магазин.
    """
    objects = models.Manager()

    SHELF_LIFE = (
        (1, '5 суток при температуре от +2 до +5 °C'),
        (2, '48 часов при температуре от +2 до +5 °C'),
        (3, '72 часа при температуре от +2 до +5 °C')
    )

    image = models.ImageField(upload_to='static/image/%Y/%m/%d/', verbose_name='Изображение')
    product_name = models.CharField(max_length=50, verbose_name='Наименование')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(verbose_name='Полное описание')
    recipe = models.OneToOneField(Recipes, on_delete=models.PROTECT, verbose_name="Рецепт")
    shelf_life = models.IntegerField(choices=SHELF_LIFE, default=0, verbose_name='Срок годности')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    cities = models.ManyToManyField(Cities, verbose_name='Города обслуживания')
    menu_categories = models.ManyToManyField('MenuCategories', verbose_name='Категория товара')
    queue = models.IntegerField(editable=False, default=0, verbose_name='Популярность')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    publication = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        """
        Метаданные для модели продукции.
        """
        db_table = 'products'
        verbose_name = 'товар'
        verbose_name_plural = 'Продукция'
        ordering = ['id']

    def __str__(self):
        """
        Возвращает значение атрибута для каждого экземпляра модели.
        """
        return f"{self.product_name}"

    def get_absolute_url(self):
        """
        Возвращает URL-адрес представления с ключевым словом "post_slug".
        """
        return reverse('product', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Прибавляет 3,7% к начальной цене, комиссия за операцию в yookassa.
        """
        commission_price = math.ceil(self.price * Decimal(1 + settings.COMMISSION))
        try:
            data = Products.objects.get(id=self.id)
            if data.price != self.price:
                self.price = commission_price
        except Products.DoesNotExist:
            self.price = commission_price
        super().save(*args, **kwargs)


class MenuCategories(models.Model):
    """
    Класс категорий продукции
    """
    objects = models.Manager()

    categorie = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    queue = models.IntegerField(verbose_name='Очередность')

    class Meta:
        """
        Метаданные для модели категорий.
        """
        db_table = 'menu_categories'
        verbose_name = 'категорию '
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        """
        Возвращает значение атрибута для каждого экземпляра модели.
        """
        return f"{self.categorie}"

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для экземпляра MenuCategories.
        """
        return reverse('category', kwargs={'cat_slug': self.slug})
