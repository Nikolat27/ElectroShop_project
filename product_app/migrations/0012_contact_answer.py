# Generated by Django 4.2.3 on 2023-09-25 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0011_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='answer',
            field=models.TextField(blank=True, null=True),
        ),
    ]
