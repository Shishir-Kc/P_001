import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE','Shree_Rastriya_Secondary_School.settings')

app =Celery('Shree_Rastriya_Secondary_School')


app.config_from_object('django.conf:settings',namespace="CELERY")

app.autodiscover_tasks()
