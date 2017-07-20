import calendar
import datetime
from random import randint

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save

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
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
]

def random(chore):
    number_of_days = randint(0, 6)
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    return date


def first(chore):
    addendum = 0
    if chore.interval == 'Monthly':
        addendum = 1
    elif chore.interval == 'Every 2 Months':
        addendum = 2
    elif chore.interval == 'Quarterly':
        addendum = 3
    elif chore.interval == 'Yearly':
        addendum = 12

    month = chore.last_assigned.month + addendum
    print("==first sub_interval month = {}".format(month))
    if month > 12:
        month = month - 12
        year = chore.last_assigned.year + 1
    else:
        year = chore.last_assigned.year
    first = datetime.date(year, month, 1)

    if THIS_WEEK.start_date <= first <= THIS_WEEK.end_date:
        return first
    else:
        return None

def fifteenth(chore):
    addendum = 0
    if chore.interval == 'Monthly':
        addendum = 1
    elif chore.interval == 'Every 2 Months':
        addendum = 2
    elif chore.interval == 'Quarterly':
        addendum = 3
    elif chore.interval == 'Yearly':
        addendum = 12

    month = chore.last_assigned.month + addendum
    if month > 12:
        month = month - 12
        year = chore.last_assigned.year + 1
    else:
        year = chore.last_assigned.year
    fifteenth = datetime.date(year, month, 15)

    if THIS_WEEK.start_date <= fifteenth <= THIS_WEEK.end_date:
        return fifteenth
    else:
        return None

def weekday(chore):
    number_of_days = randint(0, 4)
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    return date

def weekend(chore):
    number_of_days = randint(5, 6)
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    return date

def sunday(chore):
    number_of_days = 6
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    return date

def monday(chore):
    number_of_days = 0
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    return date


def tuesday(chore):
    number_of_days = 1
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    return date

def wednesday(chore):
    number_of_days = 2
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    return date

def thursday(chore):
    number_of_days = 3
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    return date

def friday(chore):
    number_of_days = 4
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
    return date

def saturday(chore):
    number_of_days = 5
    date = THIS_WEEK.start_date + datetime.timedelta(days=number_of_days)
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

def create_repeating_assignments(chore, week_start_date, increment):
    today = datetime.date.today()
    max = ((week_start_date+datetime.timedelta(days=7)) - today).days
    for d in range(0, max, increment):
        create_assignment(chore, today)
        today = today + datetime.timedelta(days=increment)
    chore.last_assigned = today
    chore.save(update_fields=['last_assigned'])

def daily(chore):
    create_repeating_assignments(chore, THIS_WEEK.start_date, 1)

def every2days(chore):
    since = THIS_WEEK.start_date - chore.last_assigned
    between = datetime.timedelta(days=2)
    if since == between:
        create_repeating_assignments(chore, THIS_WEEK.start_date, 2)
    else:
        date = THIS_WEEK.start_date + datetime.timedelta(days=1)
        create_repeating_assignments(chore, date, 2)

def every3days(chore):
    since = THIS_WEEK.start_date - chore.last_assigned
    between = datetime.timedelta(days=3)
    if since == between:
        create_repeating_assignments(chore, THIS_WEEK.start_date, 3)
    elif since - between == 1:
        date = THIS_WEEK.start_date + datetime.timedelta(days=1)
        create_repeating_assignments(chore, date, 3)
    else:
        date = THIS_WEEK.start_date + datetime.timedelta(days=2)
        create_repeating_assignments(chore, date, 3)

def weekly(chore):
    # need to check last_assigned and make sure new date is at least 5 days later
    new_date = get_date_from_subInterval(chore)
    if new_date:
        if chore.sub_interval == 'Random':
            diff_in_days = new_date - chore.last_assigned
            while diff_in_days.days < 5:
                new_date = new_date + datetime.timedelta(days=1)
                diff_in_days = new_date - chore.last_assigned
        chore.last_assigned = new_date
        chore.save(update_fields=['last_assigned'])
        create_assignment(chore, new_date)

def every2weeks(chore):
    last_week_end_date = THIS_WEEK.start_date - datetime.timedelta(days=1)
    last_week_start_date = last_week_end_date - datetime.timedelta(days=6)
    if chore.last_assigned < last_week_start_date:
        new_date = get_date_from_subInterval(chore)
        chore.last_assigned = new_date
        chore.save(update_fields=['last_assigned'])
        create_assignment(chore, new_date)
    else:
        print('{} should not be assigned this week'.format(chore.task))


def monthly(chore):
    new_date = get_date_from_subInterval(chore)
    if chore.sub_interval == '1st' or chore.sub_interval == '15th':
        if new_date:
            chore.last_assigned = new_date
            chore.save(update_fields=['last_assigned'])
            create_assignment(chore, new_date)
    else:
        if THIS_WEEK.start_date - chore.last_assigned >= datetime.timedelta(days=28):
        # difference = new_date - chore.last_assigned
        # if difference > datetime.timedelta(weeks=4, days=1):
            chore.last_assigned = new_date
            chore.save(update_fields=['last_assigned'])
            create_assignment(chore, new_date)
        else:
            print('{} should not be assigned this week'.format(chore.task))

def every2months(chore):
    new_date = get_date_from_subInterval(chore)
    print("every2months called with newdate of {}".format(new_date))
    if chore.sub_interval == '1st' or chore.sub_interval == '15th':
        if new_date:
            if new_date.year == chore.last_assigned.year:
                if new_date.month - chore.last_assigned.month == 2:
                    print("2month 1st is assigned")
                    chore.last_assigned = new_date
                    chore.save(update_fields=['last_assigned'])
                    create_assignment(chore, new_date)
            else:
                if chore.last_assigned.month - new_date.month == 10:
                    print("2month 1st is assigned")
                    chore.last_assigned = new_date
                    chore.save(update_fields=['last_assigned'])
                    create_assignment(chore, new_date)
    else:
        if THIS_WEEK.start_date - chore.last_assigned >= datetime.timedelta(weeks=8):
            chore.last_assigned = new_date
            chore.save(update_fields=['last_assigned'])
            create_assignment(chore, new_date)

def quarterly(chore):
    new_date = get_date_from_subInterval(chore)
    if chore.sub_interval == '1st' or chore.sub_interval == '15th':
        if new_date:
            if new_date.year == chore.last_assigned.year:
                if new_date.month - chore.last_assigned.month == 3:
                    chore.last_assigned = new_date
                    chore.save(update_fields=['last_assigned'])
                    create_assignment(chore, new_date)
            else:
                if chore.last_assigned.month - new_date.month == 9:
                    chore.last_assigned = new_date
                    chore.save(update_fields=['last_assigned'])
                    create_assignment(chore, new_date)
    else:
        if THIS_WEEK.start_date - chore.last_assigned >= datetime.timedelta(weeks=13):
            print("QUARTERLY new_date = {}".format(new_date))
            chore.last_assigned = new_date
            chore.save(update_fields=['last_assigned'])
            create_assignment(chore, new_date)

def yearly(chore):
    new_date = get_date_from_subInterval(chore)
    if chore.sub_interval == '1st' or chore.sub_interval == '15th':
        if new_date:
            if new_date.year > chore.last_assigned.year:
                chore.last_assigned = new_date
                chore.save(update_fields=['last_assigned'])
                create_assignment(chore, new_date)
    else:
        difference = new_date - chore.last_assigned
        if difference > datetime.timedelta(weeks=52):
            chore.last_assigned = new_date
            chore.save(update_fields=['last_assigned'])
            create_assignment(chore, new_date)
        else:
            print('{} should not be assigned this week'.format(chore.task))


#========================================================================
assigning_methods = {
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
    """
        Called when a new week is created.
        Gathers all chores, looks at their intervals and calls appropriate method.
    """
    chores = Chore.objects.filter(user=THIS_WEEK.user)
    if len(chores) > 0:
        for chore in chores:
            for choice in INTERVAL_CHOICES:
                if chore.interval == choice[0]:
                    method_name = choice[0].replace(' ', '').lower()
                    assigning_methods[method_name](chore)
    else:
        print('You have no chores to assign!')

def single_chore_added(chore, week):
    """
        if a new chore is created after a week exists,
        and new chore's interval is weekly or less:
        this creates an assignment for the current week.
    """
    global THIS_WEEK
    THIS_WEEK = week
    for choice in INTERVAL_CHOICES:
        if chore.interval == choice[0]:
            method_name = choice[0].replace(' ', '').lower()
            print(method_name)
            assigning_methods[method_name](chore)

    assign_people_to_chores()



#========================================================================
def assign_people_to_chores():
    people = Person.objects.filter(user__exact=THIS_WEEK.user)
    if len(people) > 0:
        to_dos = Assignment.objects.filter(week__exact=THIS_WEEK).filter(who__isnull = True)
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
                if all(tried):
                    working = False
                    print('Does age_restriction trump day_off or the other way around?')
            to_do.who = people[choice]
            to_do.save(update_fields=['who'])
            people[choice].weekly_minutes += to_do.what.duration
            people[choice].save(update_fields=['weekly_minutes'])
    else:
        print('You have no people to whom you may assign chores.')


#========================================================================
@receiver(post_save, sender=Week)
def week_post_save(sender, instance, created, **kwargs):
    if created:
        global TOTAL_MINUTES_GATHERED
        TOTAL_MINUTES_GATHERED = 0
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
        print("ENDED - {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        THIS_WEEK.save()
