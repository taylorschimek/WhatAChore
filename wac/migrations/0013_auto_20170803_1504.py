# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-03 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wac', '0012_auto_20170803_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='chore_icon_location',
            field=models.FilePathField(default='00_Default.png', match='.\\.png', max_length=255, path='wac/filepaths'),
        ),
    ]