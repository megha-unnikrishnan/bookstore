# Generated by Django 4.2.11 on 2024-04-26 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0007_rename_zip_code_useraddress_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referral_code',
            field=models.CharField(blank=True, default='ESTORE', max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='referred_by',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
