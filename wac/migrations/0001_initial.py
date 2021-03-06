# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-22 14:15
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import wac.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateField(null=True)),
                ('done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Chore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration', models.IntegerField()),
                ('interval', models.CharField(choices=[('Once', 'Once'), ('Daily', 'Daily'), ('Every 2 Days', 'Every 2 Days'), ('Every 3 Days', 'Every 3 Days'), ('Weekly', 'Weekly'), ('Every 2 Weeks', 'Every 2 Weeks'), ('Monthly', 'Monthly'), ('Every 2 Months', 'Every 2 Months'), ('Quarterly', 'Quarterly'), ('Yearly', 'Yearly')], default='week', max_length=15)),
                ('sub_interval', models.CharField(choices=[('None', 'None'), ('Random', 'Random'), ('1st', '1st of the month'), ('15th', '15th of the month'), ('Weekday', 'Weekday'), ('Weekend', 'Weekend'), ('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tueday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], default='random', max_length=15)),
                ('last_assigned', models.DateField(blank=True, null=True)),
                ('age_restriction', models.IntegerField()),
                ('chore_icon_location', models.FilePathField(default='Chore_Default.png', path='/Users/HOME/Developer/WAC/whatachore/wac/static/wac/styles/images/Icons/cream_icons')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='chores', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('birthday', models.DateField(default=datetime.date.today)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('day_off', models.CharField(choices=[('None', 'None'), ('Sun', 'Sunday'), ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thur', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday')], default='None', max_length=15)),
                ('mugshot', models.ImageField(blank=True, null=True, upload_to=wac.models.Person.get_image_path)),
                ('number_of_chores', models.IntegerField(blank=True, editable=False, null=True)),
                ('weekly_minutes', models.IntegerField(blank=True, editable=False, null=True)),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='people', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'people',
            },
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=False)),
                ('total_time', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='week',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wac.Week'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='what',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wac.Chore'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='who',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wac.Person'),
        ),
    ]
