import datetime
import requests

from celery import Celery
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from whatachore.utils import periodic

from useraccounts.models import User

from wac.models import Person, Week

#-SENDGRID-########################################
import sendgrid
import os
from sendgrid.helpers.mail import *




app = Celery('tasks')

app.config_from_object('django.conf:settings')

logger = get_task_logger(__name__)



# EMAIL stuff....
# password change?
# from user to worker
# after monday assignments
@app.task
def email_user(user, type):
    send_mail('What A Chore - This weeks assignments', 'Your assignments have been generated for this week.  Get to Work! \n \n \n Thanks,\nWhat A Chore Team', 'noreply@taylorschimek.com', [user.email])

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
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    if user:
        message = "To initiate password reset for " + email + ", click the link below:\n"
        message += "https://whatachore.herokuapp.com" + reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        message += '\n\n\nSincerely,\nTheWhat A Chore Team'
        email_list = [email,]

        mail = EmailMultiAlternatives(
            subject='What A Chore - Password Reset',
            body=message,
            from_email='noreply@taylorschimek.com',
            to=email_list
        )
        mail.send()

@app.task
def user_to_worker(rec_list, subject, message):
    mail = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email="noreply@taylorschimek.com",
        to=rec_list,
    )
    mail.send()


# MONDAY assignings....
@app.task
def user_assignments(user):
    try:
        new_week = Week.create(current_user=user)
        email_user(user, None)
    except ZeroDivisionError:  # the user has no workers or no chores
        pass
    logger.info("user_assignment finished = {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


@periodic_task(run_every=(crontab(hour="0", minute="15", day_of_week="monday")))
def gather_users_for_new_assignments():
    results = periodic.get_users()
    for user in results:
        user_assignments(user)
    for user in results:
        special_email_user(user, 'assigned')


@periodic_task(run_every=(crontab(hour="6-23", minute="*/15", day_of_week="*")))
def ping_self():
    logger.info("test logger on ping_self")
    r = requests.get("https://whatachore.herokuapp.com")
    return (r.status_code)














# ....
