# Generated by Django 4.2.11 on 2024-04-20 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0020_alter_editions_options'),
        ('cart', '0014_cart_coupon_cart_tax'),
        ('userapp', '0007_rename_zip_code_useraddress_zipcode'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=200)),
                ('subtotal', models.FloatField(blank=True)),
                ('order_total', models.FloatField()),
                ('discount_amount', models.FloatField(blank=True, default=0)),
                ('tax', models.FloatField()),
                ('status', models.CharField(choices=[('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Returned', 'Returned'), ('Return processing', 'Return processing'), ('Out for delivery', 'Out for delivery'), ('Order confirmed', 'Order confirmed'), ('Return requested', 'Return requested'), ('Cancelled', 'Cancelled')], default='Order confirmed', max_length=50)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userapp.useraddress')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.coupons')),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.payments')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('product_price', models.FloatField()),
                ('ordered', models.BooleanField(default=False)),
                ('return_request', models.BooleanField(default=False)),
                ('return_accept', models.BooleanField(default=False)),
                ('is_returned', models.BooleanField(default=False)),
                ('return_reason', models.TextField(blank=True)),
                ('item_cancel', models.BooleanField(blank=True, default=False, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('order_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.order')),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.payments')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.bookvariant')),
            ],
        ),
    ]