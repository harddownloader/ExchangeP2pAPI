import json
import os
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import datetime
from pymongo import MongoClient


logger = get_task_logger(__name__)


@shared_task(bind=True)
def run_partner_radar_task(self):
    try:
        logger.info(f"start run_partner_radar_task")
        with MongoClient(os.getenv('MONGODB_CONNECTION_STRING')) as connection:
            db = connection.app
            collection = db.google_sheets_config

            # is triggers active
            is_active_trigger_gs_record = collection.find_one({"name": "is_active_trigger_gs"})
            is_active_trigger_gs = is_active_trigger_gs_record['is_active_trigger_gs']
            logger.info(f"is_active_trigger_gs is {is_active_trigger_gs}")

            # get and use trigger info
            partner_radar_runner_record = collection.find_one({"name": "partner_radar_runner"})
            url = partner_radar_runner_record['endpoint']['url']
            method = partner_radar_runner_record['endpoint']['method']
            logger.info(f"partner radar URL: {url}")
            logger.info(f"partner radar METHOD: {method}")
            if (is_active_trigger_gs):
                r = requests.post(url)
                logger.info(f"request status: {r.status_code}")
                run_dashboard_radars_task.delay()

        return json.dumps({
            "status": is_active_trigger_gs
        })
    except Exception as e:
        logger.error('run_partner_radar_task error exception, please try again.')
        raise self.retry(exc=e, countdown=5)

@shared_task(bind=True)
def run_dashboard_radars_task(self):
    try:
        logger.info(f"start run_dashboard_radars_task")
        with MongoClient(os.getenv('MONGODB_CONNECTION_STRING')) as connection:
            db = connection.app
            collection = db.google_sheets_config

            # is triggers active
            is_active_trigger_gs_record = collection.find_one({"name": "is_active_trigger_gs"})
            is_active_trigger_gs = is_active_trigger_gs_record['is_active_trigger_gs']
            logger.info(f"is_active_trigger_gs is {is_active_trigger_gs}")

            # get and use trigger info
            dashboard_radars_runner_record = collection.find_one({"name": "dashboard_radars_runner"})
            url = dashboard_radars_runner_record['endpoint']['url']
            method = dashboard_radars_runner_record['endpoint']['method']
            logger.info(f"dashboard radars URL: {url}")
            logger.info(f"dashboard radars METHOD: {method}")
            if (is_active_trigger_gs):
                r = requests.get(url)
                logger.info(f"request status: {r.status_code}")
                run_partner_radar_task.delay()

        return json.dumps({
            "status": is_active_trigger_gs
        })
    except Exception as e:
        logger.error('run_dashboard_radars_task error exception, please try again.')
        raise self.retry(exc=e, countdown=5)
