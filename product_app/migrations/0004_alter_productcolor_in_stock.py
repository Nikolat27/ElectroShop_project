# Generated by Django 5.0.4 on 2024-05-06 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0003_remove_product_in_stock_productcolor_in_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcolor',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
    ]
