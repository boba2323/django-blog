# https://blog.knoldus.com/how-to-send-email-using-celery-in-django-application/
# refernece
from celery import Celery
from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

import logging
logger = logging.getLogger(__name__) # for debugging
from django.http import HttpResponse
# dont need this
# app = Celery('tasks', broker='redis://localhost')
# @app.task
# def add(x, y):
#     return x + y

@shared_task(bind=True)
def send_mail_celery_func(email_message_body) :
    try:
        # some logging operations
        logger.info("Attempting to send email")
        #operations
        # email_message_body would be a EmailMessage object or a EmailMultiAlternatives object
        email_message_body.send()
        return HttpResponse("Mail Sent Successfully")
    except Exception as e:
        logger.error(e)
        raise e