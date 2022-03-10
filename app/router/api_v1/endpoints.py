from fastapi import APIRouter

from app.segmentation import api as segmentation_api

api_router = APIRouter()

include_router = api_router.include_router

include_router(
    segmentation_api.router,
    prefix="/segmentation",
    tags=["segmentation"]
)
