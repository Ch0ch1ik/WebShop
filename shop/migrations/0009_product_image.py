# Generated by Django 4.1 on 2022-08-27 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_productincart_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='shop/static/media/'),
        ),
    ]
