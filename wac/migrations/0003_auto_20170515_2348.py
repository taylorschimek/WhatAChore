# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-16 04:48
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wac', '0002_auto_20170512_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '500x375', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
        migrations.AddField(
            model_name='person',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/wac/styles/images/uploaded_images/'),
        ),
    ]
