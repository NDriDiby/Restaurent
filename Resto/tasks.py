from celery.decorators import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task
def checkMe(message):
    
    """sends an email when feedback form is filled successfully"""
    return message