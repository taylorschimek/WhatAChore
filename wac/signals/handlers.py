import datetime
from random import randint

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save
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




#########################################################################
# Concerning Weeks and Assignments


@receiver(pre_save, sender=Week)
def obsolete_old_weeks(sender, instance, **kwargs):
    if not instance.pk:
        print("obsolete_old_weeks called")
        old_weeks = Week.objects.filter(
            user__exact=instance.user
        ).update(is_current=False)


THIS_WEEK = None
TOTAL_MINUTES_GATHERED = 0

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
    global TOTAL_MINUTES_GATHERED
    TOTAL_MINUTES_GATHERED += chore.duration
    new_assignment.save()

def create_repeating_assignments(chore, date, increment):
    print("loop called")
    for d in range(0, 7, increment):
        create_assignment(chore, date)
        date = date + datetime.timedelta(days=increment)

def once(chore):
    print("method once")

def daily(chore):
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
    else:
        number_of_days = randint(0, 1)
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
    for chore in Chore.objects.filter(user=THIS_WEEK.user):
        for choice in INTERVAL_CHOICES:
            if chore.interval == choice[0]:
                method_name = choice[0].replace(' ', '').lower()
                assigning_methods[method_name](chore)


def assign_people_to_chores():
    print('assigning people')
    people = Person.objects.filter(user__exact=THIS_WEEK.user)
    to_dos = Assignment.objects.filter(week__exact=THIS_WEEK)

    for person in people:
        person.weekly_minutes = 0

    number_of_people = len(people)
    for to_do in to_dos:
        person = randint(0, number_of_people-1)
        to_do.who = people[person]
        to_do.save(update_fields=['who'])
        print("to_do.what.duration = {}".format(to_do.what.duration))
        people[person].weekly_minutes += to_do.what.duration
        people[person].save(update_fields=['weekly_minutes'])




@receiver(post_save, sender=Week)
def week_post_save(sender, instance, created, **kwargs):
    if created:
        global TOTAL_MINUTES_GATHERED
        TOTAL_MINUTES_GATHERED = 0
        print('='*20)
        print('handlers - week_post_save')
        print('='*20)
        global THIS_WEEK
        THIS_WEEK = instance

        # TEMP - delete all assignments per user.
        Assignment.objects.exclude(week=THIS_WEEK).delete()

        get_chores_for_this_week()
        assign_people_to_chores()

        THIS_WEEK.is_current = True
        THIS_WEEK.total_time = TOTAL_MINUTES_GATHERED
        THIS_WEEK.save()
        print(Assignment.objects.filter(week=THIS_WEEK))

        # TEMP
        print(THIS_WEEK.total_time)
