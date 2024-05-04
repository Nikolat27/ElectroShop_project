# Generated by Django 5.0.2 on 2024-05-03 21:10

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account_app', '0003_delete_userwithcart'),
        ('product_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_cart', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('subtotal', models.FloatField(default=0)),
                ('coupon_used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, unique=True)),
                ('discount_percentage', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('limit_price', models.IntegerField(default=10)),
                ('maximum_price', models.IntegerField(default=1000000)),
                ('valid_from', models.DateTimeField(verbose_name='Start at')),
                ('valid_to', models.DateTimeField(verbose_name='Expire at')),
                ('active', models.BooleanField(help_text='If you wanna this coupon be available tick this field')),
                ('expired', models.BooleanField(default=False, editable=False)),
                ('maximum_use', models.IntegerField(default=1)),
                ('number_of_times_used', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=30)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.BigIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart_app.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='product_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupon_used', to='cart_app.coupon'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('postal_code', models.IntegerField()),
                ('phone_number', models.CharField(max_length=11)),
                ('subtotal', models.FloatField()),
                ('is_paid', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('unpaid', 'unpaid'), ('paid', 'paid'), ('refund', 'refund')], default='unpaid', max_length=20)),
                ('order_code', models.CharField(max_length=20, unique=True)),
                ('optional_notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=30)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.BigIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='cart_app.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart_app.province')),
            ],
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refund_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('refund_reason', models.TextField(blank=True, null=True)),
                ('refunded_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refund_order', to='cart_app.order')),
            ],
        ),
    ]
