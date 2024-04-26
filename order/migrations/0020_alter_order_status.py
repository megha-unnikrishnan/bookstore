# Generated by Django 4.2.11 on 2024-04-26 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order confirmed', 'Order confirmed'), ('Return processing', 'Return processing'), ('Return requested', 'Return requested'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Out for delivery', 'Out for delivery'), ('Returned', 'Returned')], default='Order confirmed', max_length=50),
        ),
    ]