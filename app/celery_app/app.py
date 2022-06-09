from functools import wraps

from celery import Celery, current_task

from app import settings

celery_app = Celery(
    "text_analysis",
    backend=settings.celery_backend_db,
    broker=settings.celery_broker
)

celery_app.autodiscover_tasks(
    [
        "app.segmentation",
        "app.workflows.routines"
    ]
)

celery_app.conf.task_default_queue = "text_analysis"

celery_app.conf.update(task_track_started=True)


def update_task_run(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        name = args[0].name
        percentage = args[0].percentage

        current_task.update_state(
            state="PROGRESS",
            meta={
                "process_percent": percentage,
                "message": name
            }
        )

        return function(*args, **kwargs)

    return wrapper
