# Generated by Django 4.2.11 on 2024-04-12 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_bookvariant_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='review',
            field=models.TextField(null=True),
        ),
    ]