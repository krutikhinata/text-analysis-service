from app.celery_app.app import celery_app
from app.workflows.routines.indexing.core import TaskRunner


@celery_app.task(name="document_indexing", acks_late=True)
def document_indexing(document_id: str):
    task_runner = TaskRunner()
    result = task_runner.run(document_id=document_id)

    return result
