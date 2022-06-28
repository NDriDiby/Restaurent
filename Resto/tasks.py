from celery import shared_task
from celery.schedules import crontab



@shared_task
def add(x, y):
    return x + y

