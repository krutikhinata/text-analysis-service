import uvicorn
from fastapi import FastAPI

from app import settings
from app.router.api_v1.endpoints import api_router

app = FastAPI(
    title=settings.project_name,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug
)


@app.get("/", tags=["health check"])
def health_check():
    return {"name": settings.project_name}


app.include_router(api_router, prefix=settings.api_v1_prefix)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
