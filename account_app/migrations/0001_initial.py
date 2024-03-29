# Generated by Django 4.2.3 on 2023-08-01 01:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=11, null=True, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('prof_pic', models.ImageField(blank=True, null=True, upload_to='img/prof_pics')),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('code', models.SmallIntegerField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 8, 1, 1, 53, 13, 960315, tzinfo=datetime.timezone.utc))),
                ('expiration_code', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
