from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Chore(models.Model):
    INTERVAL_CHOICES = [
        ('Daily', 'Daily'),
        ('Every 2 Days', 'Every 2 Days'),
        ('Every 3 Days', 'Every 3 Days'),
        ('Weekly', 'Weekly'),
        ('Every 2 Weeks', 'Every 2 Weeks'),
        ('Monthly', 'Monthly'),
        ('Every 2 Months', 'Every 2 Months'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly')
    ]

    SUB_INTERVAL_CHOICES = [
        ('Random', 'Random'),
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="chores", editable=False)
    task = models.CharField(max_length=25)
    description = models.TextField()
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
    chore_icon_location = models.FilePathField(default='Chore_Default.png',
                                      path='/Users/HOME/Developer/WAC/what_a_chore/wac/static/wac/styles/images/Icons/cream_icons'
    )

    def __str__(self):
        return self.name

    @property
    def chore_icon(self):
        remove = settings.BASE_DIR + '/wac/static'
        # return '/wac/styles/images/Icons/cream_icons/' + self.chore_icon_location.replace(settings.BASE_DIR, '')
        return self.chore_icon_location.replace(remove, '')



class Person(models.Model):
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="people", editable=False)
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15,
                                    validators=[phone_regex],
                                    blank=True
    )
    email = models.EmailField()
    day_off = models.CharField(max_length=15,
                               choices=DAY_OFF_CHOICES,
                               default='None'
    )
    pic_location = models.FilePathField(default='No-Current-Image.png',
                                        path='/Users/HOME/Developer/WAC/what_a_chore/wac/static/wac/styles/images/people'
    )

    def __str__(self):
        return self.name

    @property
    def person_pic(self):
        remove = settings.BASE_DIR + '/wac/static'
        # return '/wac/styles/images/Icons/cream_icons/' + self.chore_icon_location.replace(settings.BASE_DIR, '')
        return self.pic_location.replace(remove, '')

    class Meta:
        verbose_name_plural = "people"
