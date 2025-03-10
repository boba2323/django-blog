# Generated by Django 4.2.17 on 2025-02-06 16:19

import blogapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_alter_blogpost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blogpost-images/', validators=[blogapp.models.validate_image], verbose_name='Image'),
        ),
    ]
