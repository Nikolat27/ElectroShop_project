# Generated by Django 5.0.4 on 2024-05-06 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0002_remove_product_colors_remove_product_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='in_stock',
        ),
        migrations.AddField(
            model_name='productcolor',
            name='in_stock',
            field=models.BooleanField(default=False),
        ),
    ]
