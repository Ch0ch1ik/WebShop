# Generated by Django 4.1 on 2022-08-26 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_productincart_color_productincart_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productincart',
            name='color',
        ),
        migrations.RemoveField(
            model_name='productincart',
            name='size',
        ),
    ]
