"""
Модуль моделей Django в службе доставки еды для представления заказов клиентов.
"""
from django.db import models
from shop_app.models import Products
from organization.models import Cities


class Orders(models.Model):
    """
    Модель, представляющая заказы клиентов.
    """
    identifier = models.CharField(max_length=50, verbose_name='Идентификатор')
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, verbose_name='Город')
    phone = models.CharField(max_length=250, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Адрес электронной почты')
    address = models.CharField(max_length=250, verbose_name='Адрес доставки')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Время оплаты')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    work = models.BooleanField(default=False, verbose_name='В работе')
    delivered = models.BooleanField(default=False, verbose_name='Доставлен')

    class Meta:
        """
        Метаданные для модели заказов клиентов.
        """
        ordering = ('-created',)
        db_table = 'orders'
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        """
        Возвращает строковое представление заказа.
        """
        return f'Заказ {self.id}'

    def get_total_cost(self) -> float:
        """
        Рассчитывает и возвращает общую стоимость заказа.
        """
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """
    Модель, представляющая отдельные товары в заказе клиента.
    """
    order = models.ForeignKey('Orders', on_delete=models.CASCADE,
                              related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Products, on_delete=models.CASCADE,
                                related_name='order_items',
                                verbose_name='Наименование заказа')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кол-во')

    class Meta:
        """
        Метаданные для модели заказанных товаров отдельного клиента.
        """
        db_table = 'order_item'
        verbose_name = 'товар'
        verbose_name_plural = 'покупки'

    def __str__(self) -> str:
        """
        Возвращает строковое представление элемента заказа.
        """
        return f'Товары для заказа №{self.id}'

    def get_cost(self) -> float:
        """
        Рассчитывает и возвращает стоимость элемента заказа.
        """
        return self.price * self.quantity
