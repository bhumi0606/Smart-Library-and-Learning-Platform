from celery import Celery
from celery.schedules import crontab

from app.core.config import settings


celery_app = Celery(
    "smart_library",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=False,
)

celery_app.conf.beat_schedule = {
    "send-overdue-notifications-every-night": {
        "task": "send_overdue_notifications",
        "schedule": crontab(
            hour=21,
            minute=0,
        ),
        # "schedule": 10.0
    },
    "generate-monthly-library-report": {

        "task": "generate_monthly_library_report",

        "schedule": crontab(
            day_of_month=1,
            hour=8,
            minute=0,
        ),
    },
}

celery_app.autodiscover_tasks(
    [
        "app.tasks",
    ]
)

import app.tasks.overdue_notifications
import app.tasks.monthly_report