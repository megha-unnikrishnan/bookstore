# Generated by Django 4.2.11 on 2024-04-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order confirmed', 'Order confirmed'), ('Cancelled', 'Cancelled'), ('Out for delivery', 'Out for delivery'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Return processing', 'Return processing'), ('Return requested', 'Return requested'), ('Returned', 'Returned')], default='Order confirmed', max_length=50),
        ),
    ]