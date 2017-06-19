import calendar
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
        old_weeks = Week.objects.filter(
            user__exact=instance.user
        )

        if len(old_weeks) != 0:
            old_weeks.update(is_current=False)

        if len(old_weeks) == 5:
            oldest = old_weeks.order_by("start_date")[0]
            oldest.delete()



#========================================================================
SUB_INTERVAL_CHOICES = [
    ('None', 'None'),
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

def random(chore):
    print(chore.sub_interval)
    number_of_days = randint(0, 6)
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    print(date)
    return date


def first(chore):
    print(chore.sub_interval)


def fifteenth(chore):
    print(chore.sub_interval)


def weekday(chore):
    print(chore.sub_interval)
    number_of_days = randint(0, 4)
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    print(date)
    return date


def weekend(chore):
    print(chore.sub_interval)
    number_of_days = randint(5, 6)
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    print(date)
    return date


def sunday(chore):
    print(chore.sub_interval)
    number_of_days = 6
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    print(date)
    return date

def monday(chore):
    print(chore.sub_interval)
    number_of_days = 0
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    print(date)
    return date


def tuesday(chore):
    print(chore.sub_interval)
    number_of_days = 1
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    print(date)
    return date


def wednesday(chore):
    print(chore.sub_interval)
    number_of_days = 2
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    print(date)
    return date


def thursday(chore):
    print(chore.sub_interval)
    number_of_days = 3
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    print(date)
    return date


def friday(chore):
    print(chore.sub_interval)
    number_of_days = 4
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    print(date)
    return date


def saturday(chore):
    print(chore.sub_interval)
    number_of_days = 5
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    print(date)
    return date



subinterval_methods = {
    'random': random,
    '1st': first,
    '15th': fifteenth,
    'weekday': weekday,
    'weekend': weekend,
    'sunday': sunday,
    'monday': monday,
    'tuesday': tuesday,
    'wednesday': wednesday,
    'thursday': thursday,
    'friday': friday,
    'saturday': saturday,
}

def get_date_from_subInterval(chore):
    for choice in SUB_INTERVAL_CHOICES:
        if chore.sub_interval == choice[0]:
            method_name = choice[0].replace(' ', '').lower()
            date = subinterval_methods[method_name](chore)
            return date


#========================================================================
THIS_WEEK = None
TOTAL_MINUTES_GATHERED = 0

INTERVAL_CHOICES = [
    ('Once', 'Once'),
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
    chore.last_assigned = date
    chore.save(update_fields=['last_assigned'])

def once(chore):
    # Factor subinterval
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
    # need to check last_assigned and make sure new date is at least 5 days later
    new_date = get_date_from_subInterval(chore)
    print(new_date)
    chore.last_assigned = new_date
    chore.save(update_fields=['last_assigned'])
    create_assignment(chore, new_date)

def every2weeks(chore):
    print("method every 2 weeks")
    new_date = get_date_from_subInterval(chore)
    print(new_date)

def monthly(chore):
    print("method monthly")
    new_date = get_date_from_subInterval(chore)
    print(new_date)

def every2months(chore):
    print("method every 2 months")
    new_date = get_date_from_subInterval(chore)
    print(new_date)

def quarterly(chore):
    print("method quarterly")
    new_date = get_date_from_subInterval(chore)
    print(new_date)

def yearly(chore):
    print("method yearly")
    new_date = get_date_from_subInterval(chore)
    print(new_date)


#========================================================================
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

#========================================================================
def assign_people_to_chores():
    print('assigning people')
    people = Person.objects.filter(user__exact=THIS_WEEK.user)
    to_dos = Assignment.objects.filter(week__exact=THIS_WEEK)
    global TOTAL_MINUTES_GATHERED
    minute_limit = (TOTAL_MINUTES_GATHERED / len(people)) + (TOTAL_MINUTES_GATHERED / len(to_dos))

    for person in people:
        person.weekly_minutes = 0
        person.save(update_fields=['weekly_minutes'])

    for to_do in to_dos:
        working = True
        tried = [False] * len(people)
        while working:
            choice = randint(0, len(people)-1)
            tried[choice] = True

            if (
                    people[choice].age >= to_do.what.age_restriction and
                    people[choice].day_off != calendar.day_abbr[to_do.when.weekday()] and
                    people[choice].weekly_minutes < minute_limit
               ):
                working = False
                # print('+'*30)
            if all(tried):
                working = False
                print('Does age_restriction trump day_off or the other way around?')
        to_do.who = people[choice]
        to_do.save(update_fields=['who'])
        # print("to_do.what.duration = {}".format(to_do.what.duration))
        people[choice].weekly_minutes += to_do.what.duration
        people[choice].save(update_fields=['weekly_minutes'])



#========================================================================
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

        # # TEMP - delete all assignments per user.
        # Assignment.objects.filter(
        #     week__user = instance.user
        # ).exclude(
        #     week=THIS_WEEK
        # ).delete()

        get_chores_for_this_week()
        assign_people_to_chores()

        THIS_WEEK.is_current = True

        THIS_WEEK.total_time = TOTAL_MINUTES_GATHERED
        THIS_WEEK.save()

        # TEMP
        # print(THIS_WEEK.total_time)
