# Generated by Django 4.2.11 on 2024-04-22 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_alter_editions_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookvariant',
            name='max_quantity_per_person',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
