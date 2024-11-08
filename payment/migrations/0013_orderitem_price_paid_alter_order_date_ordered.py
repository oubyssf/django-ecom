# Generated by Django 5.1.2 on 2024-11-05 00:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_alter_order_date_ordered_alter_order_date_shipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price_paid',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 5, 1, 50, 7, 84109)),
        ),
    ]
