from celery import Celery

from app.core.config import CELERY_BACKEND_DB, CELERY_BROKER

celery_app = Celery(
    "main_queue",
    backend=CELERY_BACKEND_DB,
    broker=CELERY_BROKER
)

celery_app.autodiscover_tasks(
    [
        "app.segmentation"
    ]
)

celery_app.conf.update(task_track_started=True)
