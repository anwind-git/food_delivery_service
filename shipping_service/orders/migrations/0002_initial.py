# Generated by Django 5.0.2 on 2024-02-08 12:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('organization', '0001_initial'),
        ('shop_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop_app.products', verbose_name='Наименование заказа'),
        ),
        migrations.AddField(
            model_name='orders',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.cities', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='orders',
            name='delivery_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='organization.deliveryservice', verbose_name='Сотрудник службы доставки'),
        ),
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Оператор'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.orders', verbose_name='Заказ'),
        ),
    ]
