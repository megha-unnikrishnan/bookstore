# Generated by Django 4.2.11 on 2024-04-23 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_alter_bookvariant_max_quantity_per_person_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookvariant',
            name='max_quantity_per_person',
        ),
    ]