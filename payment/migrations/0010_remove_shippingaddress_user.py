# Generated by Django 5.1.2 on 2024-11-04 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_rename_date_order_date_ordered_order_date_shipped_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='user',
        ),
    ]
