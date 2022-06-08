from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    # General
    project_name: str = "text_analysis"
    version: str = "0.1.0"
    description: str = "The API for text analysis platform."

    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    # Database
    db_async_connection_str: str
    db_sync_connection_str: str
    db_exclude_tables: List[str]

    db_storage_folder: str = "storage"

    # Celery
    celery_backend_db: str
    celery_broker: str

    # Preferences
    pref_pagination: int = 10

    class Config:
        env_file = ".env"
