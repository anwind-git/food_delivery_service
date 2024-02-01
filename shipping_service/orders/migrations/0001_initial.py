# Generated by Django 5.0.1 on 2024-02-01 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Кол-во')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'покупки',
                'db_table': 'order_item',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=50, verbose_name='Идентификатор')),
                ('phone', models.CharField(max_length=250, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Адрес электронной почты')),
                ('address', models.CharField(max_length=250, verbose_name='Адрес доставки')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Последняя операция')),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('work', models.BooleanField(default=False, verbose_name='В работе')),
                ('delivered', models.BooleanField(default=False, verbose_name='Доставлен')),
                ('denial_service', models.IntegerField(blank=True, choices=[(1, 'ЗАКАЗ ОТМЕНЕН КЛИЕНТОМ'), (2, 'ЗАКАЗ НЕ ПОДТВЕРЖДЕН'), (3, 'В АДРЕСЕ ДОСТАВКИ УКАЗАН НЕ ВЕРНЫЙ ГОРОД')], default=0, null=True, verbose_name='Причина отказа в обслуживании')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'orders',
                'ordering': ('-created',),
            },
        ),
    ]
