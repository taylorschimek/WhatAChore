# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-02 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wac', '0009_auto_20170731_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='chore_icon_location',
            field=models.FilePathField(default='00_Default.png', match='.\\.png', max_length=255, path='/Users/HOME/Developer/WAC/whatachore/wac/static/wac/styles/images/icons/cream_icons'),
        ),
    ]