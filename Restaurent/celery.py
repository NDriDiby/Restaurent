import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Restaurent.settings')

app = Celery('Restaurent')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    


#Scheduling Task
app.conf.beat_schedule = {
    "add-task": {
        "task": "Resto.tasks.add_number",
        "schedule": crontab(minute="*"),
        "args":(10,10),
        
    }
}


app.conf.beat_schedule = {
    "daily-revenu": {
        "task": "Resto.tasks.get_daily_revenu",
        "schedule": crontab(minute="*"),
    }
}


app.conf.beat_schedule = {
    "transfert-amount": {
        "task": "Resto.tasks.transfert_amount",
        "schedule": crontab(minute="*"),
    }
}











