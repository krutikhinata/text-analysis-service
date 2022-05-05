from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app.core.models import StatusMessage
from app.ontologies.crud import MetricsCRUD
from app.ontologies.dependencies import get_metrics_crud
from app.ontologies.models import Metric, MetricCreate, MetricPatch

router = APIRouter()


@router.post(
    "",
    response_model=Metric,
    status_code=http_status.HTTP_201_CREATED
)
async def create_metric(
        data: MetricCreate,
        metrics: MetricsCRUD = Depends(get_metrics_crud)
):
    metric = await metrics.create(
        data=data
    )

    return metric


@router.get(
    "/{metric_id}",
    response_model=Metric,
    status_code=http_status.HTTP_201_CREATED
)
async def get_metric(
        metric_id: str,
        metrics: MetricsCRUD = Depends(get_metrics_crud)
):
    metric = await metrics.get(
        metric_id=metric_id
    )

    return metric


@router.patch(
    "/{metric_id}",
    response_model=Metric,
    status_code=http_status.HTTP_201_CREATED
)
async def patch_metric(
        metric_id: str,
        data: MetricPatch,
        metrics: MetricsCRUD = Depends(get_metrics_crud)
):
    metric = await metrics.patch(
        metric_id=metric_id,
        data=data
    )

    return metric


@router.delete(
    "/{metric_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_201_CREATED
)
async def delete_metric(
        metric_id: str,
        metrics: MetricsCRUD = Depends(get_metrics_crud)
):
    status = await metrics.delete(
        metric_id=metric_id
    )

    return {"status": status, "message": "The metric has been deleted!"}
