import os
import datetime
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver

from wac.get_username import get_username
from useraccounts.models import User


INTERVAL_CHOICES = [
    ('Daily', "Daily"),
    ('Every 2 Days', "Every 2 Days"),
    ('Every 3 Days', "Every 3 Days"),
    ('Weekly', "Weekly"),
    ('Every 2 Weeks', "Every 2 Weeks"),
    ('Monthly', "Monthly"),
    ('Every 2 Months', "Every 2 Months"),
    ('Quarterly', "Quarterly"),
    ('Yearly', "Yearly")
]

SUB_INTERVAL_CHOICES = [
    ('Random', "Random"),
    ('1st', '1st of the month'),
    ('15th', '15th of the month'),
    ('Weekday', 'Weekday'),
    ('Weekend', 'Weekend'),
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tueday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
]

DAY_OFF_CHOICES = [
    ('None', 'None'),
    ('Sun', 'Sunday'),
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thur', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday')
]


class Chore(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="chores", editable=False)
    task = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField()
    interval = models.CharField(max_length=15,
                                choices=INTERVAL_CHOICES,
                                default='week',
    )

    sub_interval = models.CharField(max_length=15,
                                    choices=SUB_INTERVAL_CHOICES,
                                    default='random',
    )

    last_assigned = models.DateField(blank=True, null=True)
    age_restriction = models.IntegerField()
    chore_icon_location = models.FilePathField(default='00_Default.png',
                                      match=".\.png",
                                      path='wac/filepaths',
                                      max_length=255
    )

    def __str__(self):
        return self.task

    @property
    def chore_icon(self):
        remove = 'filepaths'
        return self.chore_icon_location.replace(remove, '/styles/images/icons/cream_icons/')



class Person(models.Model):

    class Meta:
        verbose_name_plural = "people"

    def get_image_path(instance, filename):
        new_name = str(instance.id) + '_' + filename
        return os.path.join('people_mugs', new_name)

    def get_age(self):
        today = date.today()
        age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return age

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="people", editable=False)
    name = models.CharField(max_length=25)
    birthday = models.DateField(default=date.today)
    age = property(get_age)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(max_length=15,
    #                                 validators=[phone_regex],
    #                                 blank=True,
    #                                 null=True
    # )
    email = models.EmailField(blank=True, null=True)
    day_off = models.CharField(max_length=15,
                               choices=DAY_OFF_CHOICES,
                               default='None'
    )
    mugshot = models.ImageField(blank=True, upload_to=get_image_path, null=True)
    number_of_chores = models.IntegerField(blank=True, null=True, editable=False)
    weekly_minutes = models.IntegerField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.name

    @property
    def person_pic(self):
        print("models property")
        remove = settings.BASE_DIR + '/wac/static'
        # return '/wac/styles/images/Icons/cream_icons/' + self.chore_icon_location.replace(settings.BASE_DIR, '')
        return self.pic_location.replace(remove, '')


class Week(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_by", default=1)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    total_time = models.IntegerField(default=0)

    def prior_monday(self):
        the_date = datetime.date.today()
        idx = (the_date.weekday()) % 7
        a_monday = the_date - datetime.timedelta(days=idx)
        # if idx == 0:
        #     last_monday = a_monday - datetime.timedelta(days=7)
        #     return last_monday
        return a_monday

    @classmethod
    def create(cls, current_user):
        week = cls(user=current_user)
        week.save()

    def save(self, **kwargs):
        if not self.pk:
            self.start_date = self.prior_monday()
            self.end_date = self.start_date + datetime.timedelta(days=6)
            print("____week.start_date = {} / end_date = {}".format(self.start_date, self.end_date))

        super(Week, self).save(**kwargs)

    def __str__(self):
        return "{}'s week with pk of {}".format(self.user, self.pk)


class Assignment(models.Model):

    def __str__(self):
        return "{}'s {} - {}".format(self.when, self.what, self.done)

    week = models.ForeignKey(Week, on_delete=models.CASCADE, null=True)
    what = models.ForeignKey(Chore, on_delete=models.CASCADE, null=True)
    when = models.DateField(null=True)
    who = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    done = models.BooleanField(default=False)
