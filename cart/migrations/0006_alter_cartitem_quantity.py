# Generated by Django 4.2.11 on 2024-04-17 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_cart_cart_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.FloatField(default=0),
        ),
    ]