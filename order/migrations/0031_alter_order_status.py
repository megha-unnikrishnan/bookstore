# Generated by Django 4.2.11 on 2024-04-28 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0030_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Return processing', 'Return processing'), ('Out for delivery', 'Out for delivery'), ('Returned', 'Returned'), ('Return requested', 'Return requested'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Order confirmed', 'Order confirmed')], default='Order confirmed', max_length=50),
        ),
    ]