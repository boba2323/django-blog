# Generated by Django 4.2.17 on 2025-02-07 15:00

import blogapp.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_alter_blogpost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blogpost-images/', validators=[blogapp.models.validate_image, django.core.validators.validate_image_file_extension], verbose_name='Image'),
        ),
    ]
