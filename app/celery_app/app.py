from celery import Celery

from app import settings

celery_app = Celery(
    "main_queue",
    backend=settings.celery_backend_db,
    broker=settings.celery_broker
)

celery_app.autodiscover_tasks(
    [
        "app.segmentation"
    ]
)

celery_app.conf.update(task_track_started=True)
