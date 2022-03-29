from celery.result import AsyncResult
from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/tasks/{task_id}")
async def get_status(task_id: str):
    task_result = AsyncResult(task_id)

    result = {
        "task_id": task_id,
        "task_status": str(task_result.status),
        "task_result": task_result.result
    }

    return JSONResponse(result)
