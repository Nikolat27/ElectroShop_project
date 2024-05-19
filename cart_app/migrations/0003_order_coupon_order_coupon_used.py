# Generated by Django 5.0.4 on 2024-05-04 20:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0002_remove_cart_coupon_remove_cart_coupon_used_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart_app.coupon'),
        ),
        migrations.AddField(
            model_name='order',
            name='coupon_used',
            field=models.BooleanField(default=False),
        ),
    ]