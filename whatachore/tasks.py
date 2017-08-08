import datetime
import requests

from celery import Celery
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from templated_email import send_templated_mail, get_templated_mail

from whatachore.utils import periodic

from useraccounts.models import User

from wac.models import Assignment, Chore, Person, Week

#-SENDGRID-########################################
import sendgrid
import os
from sendgrid.helpers.mail import *

# sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
# from_email = Email("test@example.com")
# to_email = Email("test@example.com")
# subject = "Sending with SendGrid is Fun"
# content = Content("text/plain", "and easy to do anywhere, even with Python")
# mail = Mail(from_email, subject, to_email, content)
# response = sg.client.mail.send.post(request_body=mail.get())
# print(response.status_code)
# print(response.body)
# print(response.headers)
###################################################



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

@app.task
def special_email_user(user, type):
    from_email = 'noreply@taylorschimek.com'
    user_person = Person.objects.get(
        email = user.email
    )
    name = user_person.name
    current_week = Week.objects.filter(
        user = user
    ).filter(
        is_current = True
    )
    ctx = {
        'email': user.email,
        'name': name,
        'week': current_week
    }

    if type == 'welcome':
        send_templated_mail(
            template_name='welcome',
            from_email=from_email,
            recipient_list=[user.email],
            context=ctx
        )
    elif type == 'assigned':
        send_templated_mail(
            template_name='assignments',
            from_email=from_email,
            recipient_list=[user.email],
            context=ctx
        )

@app.task
def pw_email(email, token):
    user = User.objects.get(email=email)
    if user:
        ctx = {
            'email': email,
            'domain': 'localhost:8000',
            'site_name': 'What A Chore',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,  # default_token_generator.make_token(user),
            'protocol': 'http',
        }
        from_email = 'noreply@taylorschimek.com'
        try:
            send_templated_mail(
                template_name='reset_pass',
                from_email=from_email,
                recipient_list=[email],
                context=ctx
            )
        except AttributeError:
            print("attributeerror")


@app.task
def user_to_worker(rec_list, subject, message):
    sg = sendgrid.SendGridAPIClient(apikey='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')
    from_email = Email('noreply@taylorschimek.com')
    to_email = Email(rec_list[0])
    subject = subject
    content = Content('text/plain', message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


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
    logger.info("user_assignment finished = {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

# below is testing line

# below is real line
# @periodic_task(run_every=(crontab(hour=0, minute=0, day_of_week="Monday")))
@periodic_task(run_every=(crontab(hour="23", minute="30", day_of_week="sunday")))
def gather_users_for_new_assignments():
    # logger.info("Starting gufna at {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    results = periodic.get_users()
    for user in results:
        user_assignments(user)
    for user in results:
        special_email_user(user, 'assigned')
    # logger.info("Task finished at {}: week = {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), results))

@periodic_task(run_every=(crontab(hour="3", minute="*/5", day_of_week="*")))
def ping_self():
    logger.info("test logger on ping_self")
    print("BLAHing")
    r = requests.get("https://whatachore.herokuapp.com")
    return (r.status_code)














# ....
