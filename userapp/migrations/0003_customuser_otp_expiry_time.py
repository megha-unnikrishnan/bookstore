# Generated by Django 4.2.11 on 2024-04-14 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_alter_customuser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='otp_expiry_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]