from django.db import models


# сведения о руководителе, юр. лице, владельце магазина, организации
class NewManager(models.Model):
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
        db_table = 'about_manager'
        verbose_name = 'руководителя'
        verbose_name_plural = 'О руководителе'

    def __str__(self):
        return self.last_name


# адреса деятельности магазина, ресторана, организации
class Addresses(models.Model):
    city = models.ForeignKey('Cities', on_delete=models.CASCADE, verbose_name='Город')
    addresse = models.CharField(max_length=250, db_index=True, blank=False, verbose_name='Адрес ресторана')

    class Meta:
        db_table = 'addresses'
        verbose_name = 'адрес'
        verbose_name_plural = 'Адреса ресторанов'

    def __str__(self):
        return self.addresse


# города деятельности магазина, ресторана, организации
class Cities(models.Model):
    city = models.CharField(max_length=70, verbose_name='Город')
    slug = models.SlugField(max_length=70, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        db_table = 'cities'
        verbose_name = 'Город'
        verbose_name_plural = 'Города обслуживания'

    def __str__(self):
        return self.city


def cities_data():
    Cities(city='Москва', slug='moskva').save()
    Cities(city='Ростов-на-Дону', slug='rostov-na-donu').save()
    Cities(city='Краснодар', slug='krasnodar').save()


def addresses_data():
    Addresses(city=Cities.objects.get(id=1), addresse='г. Москва, ул. Совхозная, дом 39').save()
    Addresses(city=Cities.objects.get(id=2), addresse='Ростовская область, г. Ростов-на-Дону, пр. Михаила Нагибина, 32 ж').save()
    Addresses(city=Cities.objects.get(id=3), addresse='Краснодарский край, г. Краснодар, ул. имени Буденного, дом 2').save()


def manager_data():
    m1, create = NewManager.objects.get_or_create(last_name='Лукянова', first_name='Марина', middle_name='Сергеевна',
                                                  registration_form='ИП',
                                                  INN=100000000000, OGRN=100000000000000,
                                                  email='email@mail.ru',
                                                  phone='+7 (000) 000-00-00')
    m1.addresses.add(Addresses.objects.get(id=1), Addresses.objects.get(id=2), Addresses.objects.get(id=3))
    m1.save()

    m2, create = NewManager.objects.get_or_create(last_name='Дмитриенко', first_name='Николай', middle_name='Иванович',
                                                  registration_form='ИП',
                                                  INN=111111111111, OGRN=111111111111111,
                                                  email='email@mail.ru',
                                                  phone='+7 (111) 111-11-11')
    m2.addresses.add(Addresses.objects.get(id=1), Addresses.objects.get(id=2), Addresses.objects.get(id=3))
    m2.save()
