# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-16 05:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wac', '0003_auto_20170515_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(blank=True, upload_to='../whatachore/media'),
        ),
    ]
