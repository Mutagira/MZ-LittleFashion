# Generated by Django 5.1.7 on 2025-05-24 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_rename_date_order_order_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
