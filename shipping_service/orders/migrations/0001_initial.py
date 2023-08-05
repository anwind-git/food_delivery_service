# Generated by Django 4.2.3 on 2023-08-05 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop_app', '0001_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=50, verbose_name='Идентификатор')),
                ('phone', models.CharField(max_length=250, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Адрес электронной почты')),
                ('address', models.CharField(max_length=250, verbose_name='Адрес доставки')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Время оплаты')),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('work', models.BooleanField(default=False, verbose_name='В работе')),
                ('delivered', models.BooleanField(default=False, verbose_name='Доставлен')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.cities', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'orders',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Кол-во')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.orders', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop_app.products', verbose_name='Наименование заказа')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'покупки',
                'db_table': 'order_item',
            },
        ),
    ]
