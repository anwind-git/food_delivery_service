"""
Модуль моделей Django в службе доставки еды для хранения сведений об организации.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    Класс представляет модель пользователей системы. Включая суперпользователя.
    """
    city = models.ForeignKey('Cities', null=True, on_delete=models.PROTECT, verbose_name='Город')
    address = models.ForeignKey('Addresses', null=True, on_delete=models.PROTECT, verbose_name='Адрес')
    phone = models.CharField(max_length=20, blank=False, verbose_name='Телефон')


class NewManager(models.Model):
    """
    Класс представляет данные руководителя организации.
    """
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    middle_name = models.CharField(max_length=30, verbose_name='Отчество')
    registration_form = models.CharField(max_length=50, verbose_name='Форма регистрации')
    addresses = models.ManyToManyField('Addresses', verbose_name='Адреса ресторанов')
    INN = models.PositiveBigIntegerField(verbose_name='ИНН')
    OGRN = models.PositiveBigIntegerField(verbose_name='ОГРН')
    phone = models.CharField(max_length=20, blank=False, verbose_name='Телефон')
    email = models.CharField(max_length=50, verbose_name='Электронная почта')

    class Meta:
        """
        Метаданные для модели руководителя организации.
        """
        db_table = 'about_manager'
        verbose_name = 'руководителя'
        verbose_name_plural = 'О руководителе'

    def __str__(self):
        """
        Возвращает строковое представление фамилии руководителя организации.
        """
        return self.last_name


class Addresses(models.Model):
    """
    Представляет адреса, в которых работает магазин.
    """
    city = models.ForeignKey('Cities', on_delete=models.CASCADE, verbose_name='Город')
    addresse = models.CharField(max_length=250, db_index=True, blank=False, verbose_name='Адрес магазина')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    working_time = models.CharField(max_length=16, verbose_name='Время работы')

    class Meta:
        """
        Метаданные для модели адресов.
        """
        db_table = 'addresses'
        verbose_name = 'адрес'
        verbose_name_plural = 'Адреса магазинов'

    def __str__(self):
        """
        Возвращает строковое представление рабочего адреса ресторана.
        """
        return self.addresse


class Cities(models.Model):
    """
    Модель данных городов, в которых работает магазин.
    """
    city = models.CharField(max_length=70, verbose_name='Город')
    slug = models.SlugField(max_length=70, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        """
        Метаданные для модели городов.
        """
        db_table = 'cities'
        verbose_name = 'Город'
        verbose_name_plural = 'Города обслуживания'

    def __str__(self):
        """
        Возвращает строковое представление города.
        """
        return self.city


class DeliveryService(models.Model):
    """
    Класс представляет города, в которых работает магазин.
    """
    fio = models.CharField(max_length=100, verbose_name='ФИО')
    age = models.IntegerField(verbose_name='Возраст')
    phone = models.CharField(max_length=20, blank=False, verbose_name='Телефон')
    telegram = models.CharField(max_length=100, verbose_name='Telegram')
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, verbose_name='Город')
    manager = models.ForeignKey(NewManager, null=True, on_delete=models.PROTECT, verbose_name='Руководитель')
    status = models.BooleanField(default=False, verbose_name='На доставке')
    day_off = models.BooleanField(default=False, verbose_name='Выходной')
    work_authorization = models.BooleanField(default=False, verbose_name='Допущен к работе')
    additional_information = models.TextField(null=True, blank=True, verbose_name='Дополнительная информация')

    class Meta:
        """
        Метаданные для модели службы доставки.
        """
        db_table = 'delivery_service'
        verbose_name = 'сотрудника'
        verbose_name_plural = 'Служба доставки'

    def __str__(self):
        """
        Возвращает ФИО сотрудника службы доставки.
        """
        return self.fio
