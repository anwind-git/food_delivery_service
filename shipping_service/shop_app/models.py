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
    recipe = models.ForeignKey(Recipes, on_delete=models.PROTECT, verbose_name='Рецепт')
    shelf_life = models.IntegerField(choices=SHELF_LIFE, default=0, verbose_name='Срок годности')
    price = models.IntegerField(verbose_name='Цена')
    cities = models.ManyToManyField(Cities, verbose_name='Города обслуживания')
    menu_categories = models.ManyToManyField('MenuCategories', verbose_name='Категория товара')
    queue = models.IntegerField(editable=False, default=0, verbose_name='Очередность')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    publication = models.BooleanField(default=True, verbose_name='Опубликовано')

    # метаданные для модели
    class Meta:
        db_table = 'products'
        verbose_name = 'товар'
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
        try:
            data = Products.objects.get(id=self.id)
            if data.price != self.price:
                self.price = commission_calculation(self)
        except Products.DoesNotExist:
            self.price = commission_calculation(self)
        super().save(*args, **kwargs)


def commission_calculation(data):
    price = math.ceil(data.price * Decimal(1 + 0.037))
    return price


# класс категорий меню товаров
class MenuCategories(models.Model):
    categorie = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    queue = models.IntegerField(verbose_name='Очередность')

    class Meta:
        db_table = 'menu_categories'
        verbose_name = 'категорию '
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.categorie

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


def menu_categories_data():
    MenuCategories(categorie='популярные', slug='populyarnye', queue=1).save()
    MenuCategories(categorie='завтраки', slug='zavtraki', queue=2).save()
    MenuCategories(categorie='салаты', slug='salaty', queue=3).save()
    MenuCategories(categorie='первое', slug='pervoe', queue=4).save()
    MenuCategories(categorie='второе', slug='vtoroe', queue=5).save()
    MenuCategories(categorie='десерты', slug='deserty', queue=6).save()
    MenuCategories(categorie='выпечка', slug='vypechka', queue=7).save()
    MenuCategories(categorie='напитки', slug='napitki', queue=8).save()


def products_data():
    p1, create = Products.objects.get_or_create(image='static/image/2023/05/01/1.jpg',
             product_name='Грибной суп с кабачками',
             slug='gribnoj-sup-s-kabachkami',
             description='Горячий наваристый грибной суп с кабачками – что может быть вкуснее? Он отлично насыщает, '
                         'подходит для любого времени года, дарит необходимые микроэлементы и даже помогает справляться с '
                         'простудой и болезнями, укрепляя организм.',
             shelf_life=1, price=120, queue=0, recipe=Recipes.objects.get(id=1),
             time_create='2023-05-21 09:17:36.799849', time_update='2023-09-01 10:34:46.124096',
             publication=1)
    p1.cities.add(Cities.objects.get(id=1), Cities.objects.get(id=2), Cities.objects.get(id=3))
    p1.menu_categories.add(MenuCategories.objects.get(id=1), MenuCategories.objects.get(id=4))
    p1.save()

    p2, create = Products.objects.get_or_create(image='static/image/2023/05/01/2.jpg',
             product_name='Омлет по-болгарски',
             slug='omlet-po-bolgarski',
             description='Классическое блюдо болгарской кухни, которое можно предложить в вашем магазине как вкусную закуску '
                         'или завтрак. Омлет приготавливается из яиц, лука, перца, моркови и специй, что придает ему особый '
                         'вкус и аромат. Он является питательным и сытным блюдом, которое подойдет для разнообразных вкусовых '
                         'предпочтений. Омлет по-болгарски можно подавать в горячем виде, а также варианты с различными добавками, '
                         'например, с сыром или колбасой. Омлет по-болгарски - отличный выбор для тех, кто хочет попробовать '
                         'блюдо с насыщенным вкусом и простыми, но вкусными ингредиентами.',
            shelf_life=1, price=170, queue=0, recipe=Recipes.objects.get(id=2),
            time_create='2023-05-21 09:17:36.799849', time_update='2023-09-01 10:34:46.124096',
            publication=1)
    p2.cities.add(Cities.objects.get(id=1), Cities.objects.get(id=2), Cities.objects.get(id=3))
    p2.menu_categories.add(MenuCategories.objects.get(id=1), MenuCategories.objects.get(id=2))
    p2.save()

    p3, create = Products.objects.get_or_create(image='static/image/2023/05/01/3.jpg',
                                                product_name='Салат из морской капусты',
                                                slug='salat-iz-morskoj-kapusty',
                                                description='Богатый источник питательных веществ, включая витамины и '
                                                            'минералы. Содержит много клетчатки, что способствует '
                                                            'здоровому пищеварению. Морская капуста имеет низкую '
                                                            'калорийность, что делает этот салат отличным вариантом для '
                                                            'людей, следящих за своим весом. Насыщен вкусом и текстурой, '
                                                            'что делает его приятным для употребления.',
                                                shelf_life=1, price=140, queue=0, recipe=Recipes.objects.get(id=3),
                                                time_create='2023-05-21 09:17:36.799849',
                                                time_update='2023-09-01 10:34:46.124096',
                                                publication=1)
    p3.cities.add(Cities.objects.get(id=1), Cities.objects.get(id=2), Cities.objects.get(id=3))
    p3.menu_categories.add(MenuCategories.objects.get(id=1), MenuCategories.objects.get(id=3))
    p3.save()

    p4, create = Products.objects.get_or_create(image='static/image/2023/05/01/4.jpg',
                                                product_name='Творог с ягодами',
                                                slug='tvorog-s-yagodami',
                                                description='Вкусный десерт, который сочетает в себе нежный творог и '
                                                            'ароматные ягоды. Творог является основным ингредиентом этого '
                                                            'блюда и служит источником белка, кальция и других полезных '
                                                            'питательных веществ. Ягоды, такие как клубника, придают '
                                                            'блюду яркий цвет, свежий вкус и аромат.',
                                                shelf_life=1, price=120, queue=0, recipe=Recipes.objects.get(id=4),
                                                time_create='2023-05-21 09:17:36.799849',
                                                time_update='2023-09-01 10:34:46.124096',
                                                publication=1)
    p4.cities.add(Cities.objects.get(id=1), Cities.objects.get(id=2), Cities.objects.get(id=3))
    p4.menu_categories.add(MenuCategories.objects.get(id=1), MenuCategories.objects.get(id=6))
    p4.save()

    p5, create = Products.objects.get_or_create(image='static/image/2023/05/01/5.jpg',
                                                product_name='Творожный лапшевник',
                                                slug='tvorozhnyj-lapshevnik',
                                                description='Может подаваться как горячим, так и холодным. Он может '
                                                            'быть украшен свежими ягодами, мятой или посыпан орехами для'
                                                            ' добавления визуальной привлекательности и дополнительного '
                                                            'вкуса. Это блюдо отлично подходит для тех, кто любит '
                                                            'сладкие и молочные десерты. Творожный лапшевник позволяет '
                                                            'насладиться сочетанием кремообразного творога и нежной лапши, '
                                                            'создавая приятный опыт для гурманов.',
                                                shelf_life=1, price=200, queue=0, recipe=Recipes.objects.get(id=5),
                                                time_create='2023-05-21 09:17:36.799849',
                                                time_update='2023-09-01 10:34:46.124096',
                                                publication=1)
    p5.cities.add(Cities.objects.get(id=1), Cities.objects.get(id=2), Cities.objects.get(id=3))
    p5.menu_categories.add(MenuCategories.objects.get(id=1), MenuCategories.objects.get(id=6))
    p5.save()

    p6, create = Products.objects.get_or_create(image='static/image/2023/05/01/6.jpg',
                                                product_name='Борщ с говядиной',
                                                slug='borsh-s-govyadinoj',
                                                description='Классическое украинское блюдо, которое является одним из '
                                                            'символов национальной кухни. Он известен своим насыщенным '
                                                            'вкусом, ярким цветом и разнообразием ингредиентов. Борщ '
                                                            'готовится на основе бульона из говядины, который придает '
                                                            'ему богатый и ароматный вкус. Вариации борща могут включать '
                                                            'различные овощи, такие как свекла, картофель, морковь, '
                                                            'лук и капуста.',
                                                shelf_life=1, price=170, queue=0, recipe=Recipes.objects.get(id=6),
                                                time_create='2023-05-21 09:17:36.799849',
                                                time_update='2023-09-01 10:34:46.124096',
                                                publication=1)
    p6.cities.add(Cities.objects.get(id=1), Cities.objects.get(id=2), Cities.objects.get(id=3))
    p6.menu_categories.add(MenuCategories.objects.get(id=1), MenuCategories.objects.get(id=4))
    p6.save()

    p7, create = Products.objects.get_or_create(image='static/image/2023/05/01/7.jpg',
                                                product_name='Гороховый суп с мясом',
                                                slug='gorohovyj-sup-s-myasom',
                                                description='Популярное блюдо во многих кухнях и известно своим богатым '
                                                            'вкусом и питательными свойствами. Главным ингредиентом '
                                                            'горохового супа является горох, который может быть зеленым '
                                                            'или желтым. Горох богат пищевыми волокнами, белком и '
                                                            'различными витаминами и минералами. Он придает супу '
                                                            'плотность и характерный вкус.',
                                                shelf_life=1, price=120, queue=0, recipe=Recipes.objects.get(id=7),
                                                time_create='2023-05-21 09:17:36.799849',
                                                time_update='2023-09-01 10:34:46.124096',
                                                publication=1)
    p7.cities.add(Cities.objects.get(id=1), Cities.objects.get(id=2), Cities.objects.get(id=3))
    p7.menu_categories.add(MenuCategories.objects.get(id=1), MenuCategories.objects.get(id=4))
    p7.save()
