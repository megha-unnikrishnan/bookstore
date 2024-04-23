# Generated by Django 4.2.11 on 2024-04-22 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Returned', 'Returned'), ('Cancelled', 'Cancelled'), ('Return processing', 'Return processing'), ('Return requested', 'Return requested'), ('Order confirmed', 'Order confirmed'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery')], default='Order confirmed', max_length=50),
        ),
    ]