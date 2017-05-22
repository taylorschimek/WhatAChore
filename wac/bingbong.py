from django.dispatch import receiver
from django.db.models.signals import post_save
from wac.get_username import get_username
from wac.models import Chore, Person, Week


def create_assignment(self, chore, date):
    new_assignment = Assignment.objects.create(
        # week = self, # <- this needs to be in a receiver
        what = chore,
        when = date,
    )
    new_assignment.save()


def create_repeating_assignments(self, chore, date, increment):
    print("loop called")
    for d in range(0, 7, increment):
        print(d)
        self.create_assignment(chore, date)
        date = date + datetime.timedelta(days=increment)

def __str__(self):
    return "Week with start date of {}".format(self.start_date)

def once(self, chore):
    print("method once")

def daily(self, chore):
    print("method daily")
    self.create_repeating_assignments(chore, self.start_date, 1)

def every2days(self, chore):
    print("method every 2 days")
    self.create_repeating_assignments(chore, self.start_date, 2)

def every3days(self, chore):
    print("method every 3 days")
    self.create_repeating_assignments(chore, self.start_date, 3)

def weekly(self, chore):
    print("method weekly")
    if chore.sub_interval == "Random":
        number_of_days = randint(0, 6)
        print(number_of_days)
        date = self.start_date + datetime.timedelta(days=number_of_days)
        self.create_assignment(chore, date)

def every2weeks(self, chore):
    print("method every 2 weeks")

def monthly(self, chore):
    print("method monthly")

def every2months(self, chore):
    print("method every 2 months")

def quarterly(self, chore):
    print("method quarterly")

def yearly(self, chore):
    print("method yearly")

def get_chores_for_this_week():
    req = get_username()
    print(req)
    print(sender)
    # for chore in Chore.objects.filter(user=req.user):
    #     for choice in INTERVAL_CHOICES:
    #         if chore.interval == choice[0]:
    #             method_name = choice[0].replace(' ', '').lower()
    #             method = getattr(self, method_name)
    #             method(chore)

@receiver(post_save, sender=Week)
def week_post_save(sender, instance, **kwargs):
    print('the fucking signal worked')
    # if not sender.pk:
    #     print("Not self.pk")
    #     todays_date = datetime.date.today()
    #     idx = (todays_date.weekday() + 1) % 7
    #     if todays_date.weekday() is not 0:
    #         sender.start_date = todays_date - datetime.timedelta(idx)
    #     else:
    #         sender.start_date = todays_date
    #     sender.end_date = sender.start_date + datetime.timedelta(days=7)
    #
    #     # TEMP - delete all chores per user.
    #     # Assignment.objects.filter(week=sender).delete()
    #
    #     # self.get_chores_for_this_week()
    # else:
    #     print("self.pk")
