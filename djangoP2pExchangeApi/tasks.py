from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True)
def create_backup_task(self):
    try:
        logger.info(f"start create_backup_task")

        return True
    except Exception as e:
        logger.error('create_backup_task error exception, please try again.')
        raise self.retry(exc=e, countdown=5)
