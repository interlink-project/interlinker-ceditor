import os
import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    MONGODB_URL: str
    MONGODB_DATABASE: str
    COLLECTION_NAME: str

    ETHERPAD_API_KEY: str
    ETHERPAD_HOST: str
    ETHERPAD_PORT: int
    ETHERPAD_SERVICE: str = os.getenv("ETHERPAD_HOST") + ":" + os.getenv("ETHERPAD_PORT")

    PROTOCOL: str = "https://" if "https://" in os.getenv("SERVER_HOST", "") else "http://"

    class Config:
        case_sensitive = True


settings = Settings()
