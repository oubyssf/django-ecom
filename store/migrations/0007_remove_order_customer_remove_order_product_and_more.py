# Generated by Django 5.1.2 on 2024-11-02 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_profile'),
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
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
