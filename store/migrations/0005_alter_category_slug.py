# Generated by Django 5.1.2 on 2024-10-30 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
