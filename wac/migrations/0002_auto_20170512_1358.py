# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='chore_icon_location',
            field=models.FilePathField(default='Chore_Default.png', path='/Users/HOME/Developer/WAC/whatachore/wac/static/wac/styles/images/Icons/cream_icons'),
        ),
        migrations.AlterField(
            model_name='person',
            name='pic_location',
            field=models.FilePathField(default='No-Current-Image.png', path='/Users/HOME/Developer/WAC/whatachore/wac/static/wac/styles/images/people'),
        ),
    ]
