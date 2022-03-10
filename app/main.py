import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core import config as config
from app.router.api_v1.endpoints import api_router

app = FastAPI(title=config.PROJECT_NAME,
              openapi_url=f"{config.API_V1_PREFIX}/openapi.json",
              debug=config.DEBUG)

if config.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


@app.get("/", tags=["health check"])
def health_check():
    return {"name": config.PROJECT_NAME}


app.include_router(api_router, prefix=config.API_V1_PREFIX)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
