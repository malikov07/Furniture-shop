# Generated by Django 5.0.6 on 2024-06-17 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=1, upload_to='product_images'),
            preserve_default=False,
        ),
    ]
