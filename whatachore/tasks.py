from celery import Celery
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail

from whatachore.utils import periodic

from useraccounts.models import User

from wac.models import Chore, Person, Week


app = Celery('tasks')

app.config_from_object('django.conf:settings')

@app.task
def add(x, y):
    print("this is the sum of {} and {}".format(x, y))
    return x + y


logger = get_task_logger(__name__)


# EMAIL stuff....
# password change?
# from user to worker
# after monday assignments
@app.task
def email_user(user, type):
    send_mail('Monday Assigning Test', 'testing this nonsense', 'noreply@taylorschimek.com', [user.email])


# MONDAY assignings....
@app.task
def user_assignments(user):
    # logger.info("user_assignment called for {}".format(user))
    try:
        new_week = Week.create(current_user=user)
        # logger.info("Try succeeded")
        # email user assignments?
    except ZeroDivisionError:  # the user has no workers or no chores
        pass
        # logger.info("Try failed")
        # email user that they're missing either workers or chores and assignments cannot be made.
    logger.info("user_assignment finished = {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

# below is real line
# @periodic_task(run_every=(crontab(hour=0, minute=0, day_of_week="Monday")))
# below is testing line
@periodic_task(run_every=(crontab(hour="*", minute="*/2", day_of_week="Monday")))
def gather_users_for_new_assignments():
    logger.info("Starting gufna at {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    results = periodic.get_users()
    for user in results:
        user_assignments(user)
    for user in results:
        email_user(user, 'assigned')
    logger.info("Task finished at {}: week = {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), results))














# ....
