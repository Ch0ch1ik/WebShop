# Generated by Django 4.1 on 2022-08-26 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_cart_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='productincart',
            name='color',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='shop.colors'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productincart',
            name='size',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='shop.sizes'),
            preserve_default=False,
        ),
    ]