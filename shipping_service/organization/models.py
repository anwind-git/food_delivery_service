"""
Модуль моделей Django в службе доставки еды для хранения сведений об организации.
"""
from django.db import models


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
    addresse = models.CharField(max_length=250, db_index=True, blank=False, verbose_name='Адрес ресторана')

    class Meta:
        """
        Метаданные для модели адресов.
        """
        db_table = 'addresses'
        verbose_name = 'адрес'
        verbose_name_plural = 'Адреса ресторанов'

    def __str__(self):
        """
        Возвращает строковое представление рабочего адреса ресторана.
        """
        return self.addresse


class Cities(models.Model):
    """
    Представляет города, в которых работает магазин.
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
