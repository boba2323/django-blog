# https://medium.com/django-unleashed/asynchronous-tasks-in-django-a-step-by-step-guide-to-celery-and-docker-integration-b6f9898b66b5


# https://docs.celeryq.dev/en/latest/django/first-steps-with-django.html

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# sets "DJANGO_SETTINGS_MODULE" if it doesnt already exist
# funny it works here since we had to move the sendgrid-emailtest.py to the root of the project

app = Celery("mysite")

# all config must prefix with CELERY
app.config_from_object("django.conf:settings", namespace="CELERY")

# looks for tasks.py in all installed apps, eg it will look for blogapp/tasks.py
app.autodiscover_tasks()

# this is a sample task
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')