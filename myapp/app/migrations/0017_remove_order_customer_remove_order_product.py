# Generated by Django 5.1.7 on 2025-05-24 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_order_shipping_address_order_shipping_cost_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]
