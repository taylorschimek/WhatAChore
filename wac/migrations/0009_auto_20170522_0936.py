# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-22 14:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wac', '0008_auto_20170522_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
