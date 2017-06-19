from celery import Celery
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime
from django.conf import settings

from whatachore.utils import periodic


app = Celery('tasks')

app.config_from_object('django.conf:settings')

@app.task
def add(x, y):
    print("this is the sum of {} and {}".format(x, y))
    return x + y


logger = get_task_logger(__name__)

# A periodic task that will run every minute (the symbol '*' means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def periodic_example():
    logger.info("Start task")
    now = datetime.now()
    result = periodic.periodic_example(now.day, now.minute)
    logger.info("Task finished: result = {}".format(result))
