import logging

from fastapi import APIRouter, BackgroundTasks
from fastapi import status as http_status

from app.celery_app.app import celery_app
from app.celery_app.models import TaskCreated, TaskTrigger

router = APIRouter()


log = logging.getLogger(__name__)


def background_on_message(task):
    log.info(task.get(propagate=False))


@router.post(
    "",
    response_model=TaskCreated,
    status_code=http_status.HTTP_201_CREATED
)
async def trigger_checker(
        data: TaskTrigger,
        background_tasks: BackgroundTasks
):
    kwargs = data.parameters
    task = celery_app.send_task(data.task_name, kwargs=kwargs)
    background_tasks.add_task(background_on_message, task)

    return TaskCreated(task_id=task.id)
