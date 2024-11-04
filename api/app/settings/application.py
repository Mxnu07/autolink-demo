from typing import Union
from functools import lru_cache
from pydantic_settings import BaseSettings

class ApplicationSettings(BaseSettings):
    environment_name: str  # dev, stage, prod
    log_level: str  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    app_version: str = "no-version"
    app_release_date: str = "no-release-date"
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

@lru_cache()
def get_settings() -> ApplicationSettings:
    return ApplicationSettings()
