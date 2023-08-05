from django.db import models


class Manager(models.Model):
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    middle_name = models.CharField(max_length=30, verbose_name='Отчество')
    registration_form = models.CharField(max_length=50, verbose_name='Форма регистрации')
    organization_name = models.CharField(max_length=50, blank=False, verbose_name='Название организации')
    addresses = models.ManyToManyField('Addresses', verbose_name='Адреса ресторанов')
    INN = models.PositiveBigIntegerField(verbose_name='ИНН')
    OGRN = models.PositiveBigIntegerField(verbose_name='ОГРН')
    phone = models.CharField(max_length=20, blank=False, verbose_name='Телефон')

    class Meta:
        db_table = 'about_manager'
        verbose_name = 'руководителя'
        verbose_name_plural = 'О руководителе'

    def __str__(self):
        return self.last_name


class Addresses(models.Model):
    addresse = models.CharField(max_length=250, db_index=True, blank=False, verbose_name='Адрес ресторана')

    class Meta:
        db_table = 'addresses'
        verbose_name = 'адрес'
        verbose_name_plural = 'Адреса ресторанов'

    def __str__(self):
        return self.addresse


class Cities(models.Model):
    city = models.CharField(max_length=70, verbose_name='Город')
    slug = models.SlugField(max_length=70, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        db_table = 'cities'
        verbose_name = 'Город'
        verbose_name_plural = 'Города обслуживания'

    def __str__(self):
        return self.city
