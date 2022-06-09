from fastapi import APIRouter

from app.celery_app import api as celery_api
from app.documents import api as documents_api
from app.ontologies import api as ontologies_api
from app.segmentation import api as segmentation_api
from app.workflows import api as workflows_api

api_router = APIRouter()

include_router = api_router.include_router

routers = [
    (celery_api.router, "/celery", ["celery"]),
    (documents_api.router, "/documents", ["documents"]),
    (ontologies_api.router, "/ontologies", ["ontologies"]),
    (segmentation_api.router, "/segmentation", ["segmentation"]),
    (workflows_api.router, "/workflows", ["workflows"])
]

for router, prefix, tags in routers:
    include_router(
        router=router,
        prefix=prefix,
        tags=tags
    )
