import os
import sys

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

env_files = ["dev.env", "prod.env"]

config = Config()
for env_file in env_files:
    if os.path.exists(env_file):
        config = Config(env_file)

TEST_ENV = "pytest" in sys.modules

# Base
API_V1_PREFIX = config("API_V1_PREFIX", cast=str)
DEBUG = config("DEBUG", cast=bool)
PROJECT_NAME = config("PROJECT_NAME", cast=str)

BACKEND_CORS_ORIGINS = list(
    config("BACKEND_CORS_ORIGINS", cast=CommaSeparatedStrings)
)

# Celery
CELERY_BACKEND_DB = config("CELERY_BACKEND_DB", cast=str)
CELERY_BROKER = config("CELERY_BROKER", cast=str)
