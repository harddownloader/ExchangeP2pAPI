import os
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import datetime

logger = get_task_logger(__name__)

@shared_task(bind=True)
def run_partner_radar_task(self):
    try:
        logger.info(f"start run_partner_radar_task")

        r = requests.post(os.getenv('APP_SCRIPT_ENDPOINT'))
        run_dashboard_radars_task.delay()

        return r.status_code
    except Exception as e:
        logger.error('run_partner_radar_task error exception, please try again.')
        raise self.retry(exc=e, countdown=5)

@shared_task(bind=True)
def run_dashboard_radars_task(self):
    try:
        logger.info(f"start run_dashboard_radars_task")

        r = requests.get(
            os.getenv('APP_SCRIPT_ENDPOINT')
        )
        # call_endpoint1_task.delay()

        return r.status_code
    except Exception as e:
        logger.error('run_dashboard_radars_task error exception, please try again.')
        raise self.retry(exc=e, countdown=5)
