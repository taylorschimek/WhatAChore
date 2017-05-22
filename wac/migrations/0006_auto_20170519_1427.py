# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 19:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wac', '0005_week_is_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='chore',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wac.Chore'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='user',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to=settings.AUTH_USER_MODEL),
        ),
    ]
