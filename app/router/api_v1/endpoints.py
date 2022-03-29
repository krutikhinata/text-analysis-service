from fastapi import APIRouter

from app.celery_app import api as celery_api
from app.segmentation import api as segmentation_api

api_router = APIRouter()

include_router = api_router.include_router

include_router(
    segmentation_api.router,
    prefix="/segmentation",
    tags=["segmentation"]
)

include_router(
    celery_api.router,
    prefix="/celery",
    tags=["celery"]
)
