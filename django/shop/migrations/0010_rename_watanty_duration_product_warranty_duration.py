# Generated by Django 5.0.6 on 2024-06-18 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_order_created_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='watanty_duration',
            new_name='warranty_duration',
        ),
    ]
