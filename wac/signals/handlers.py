import datetime
from random import randint

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from wac.get_username import get_username

from wac.models import Assignment, Chore, Person, Week

# Concerning Person Images

@receiver(pre_delete, sender=Person)
def person_delete(sender, instance, **kwargs):
    print('='*20)
    print('handlers - person_delete')
    print('='*20)
    if instance.mugshot:
        instance.mugshot.delete(False)


# Concerning Weeks and Assignments

THIS_WEEK = None

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

def create_assignment(chore, date):
    new_assignment = Assignment.objects.create(
        week = THIS_WEEK,
        what = chore,
        when = date,
    )
    new_assignment.save()


def create_repeating_assignments(chore, date, increment):
    print("loop called")
    for d in range(0, 7, increment):
        print(d)
        create_assignment(chore, date)
        date = date + datetime.timedelta(days=increment)

def once(chore):
    print("method once")

def daily(self, chore):
    print("method daily")
    create_repeating_assignments(chore, THIS_WEEK.start_date, 1)

def every2days(chore):
    print("method every 2 days")
    create_repeating_assignments(chore, THIS_WEEK.start_date, 2)

def every3days(chore):
    print("method every 3 days")
    create_repeating_assignments(chore, THIS_WEEK.start_date, 3)

def weekly(chore):
    print("method weekly")
    if chore.sub_interval == "Random":
        number_of_days = randint(0, 6)
        print(number_of_days)
        date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
        create_assignment(chore, date)

def every2weeks(chore):
    print("method every 2 weeks")

def monthly(chore):
    print("method monthly")

def every2months(chore):
    print("method every 2 months")

def quarterly(chore):
    print("method quarterly")

def yearly(chore):
    print("method yearly")

assigning_methods = {
    'once': once,
    'daily': daily,
    'every2days': every2days,
    'every3days': every3days,
    'weekly': weekly,
    'every2weeks': every2weeks,
    'monthly': monthly,
    'every2months': every2months,
    'quarterly': quarterly,
    'yearly': yearly,
}

def get_chores_for_this_week():
    print(THIS_WEEK)
    print(THIS_WEEK.start_date)
    for chore in Chore.objects.filter(user=THIS_WEEK.user):
        for choice in INTERVAL_CHOICES:
            if chore.interval == choice[0]:
                method_name = choice[0].replace(' ', '').lower()
                assigning_methods[method_name](chore)

@receiver(post_save, sender=Week)
def week_post_save(sender, instance, **kwargs):
    print('='*20)
    print('handlers - week_post_save')
    print('='*20)
    global THIS_WEEK
    THIS_WEEK = instance
    print(THIS_WEEK.start_date)
    print(THIS_WEEK.end_date)
    # TEMP - delete all chores per user.
    Assignment.objects.exclude(week=THIS_WEEK).delete()

    get_chores_for_this_week()
