# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-09 03:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wac', '0015_auto_20170803_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='phone_number',
        ),
    ]
