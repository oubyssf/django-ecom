# Generated by Django 5.1.2 on 2024-11-06 20:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0016_rename_price_paid_orderitem_price_paid_per_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 21, 42, 27, 412377)),
        ),
    ]
