# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-21 04:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0003_auto_20170720_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='welcomed',
            field=models.BooleanField(default=False),
        ),
    ]