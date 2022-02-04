import os
import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

mode = os.getenv("MODE", "")
class Settings(BaseSettings):
    MODE: str
    MODE_SOLO: bool = mode == "solo"
    MODE_INTEGRATED: bool = mode == "integrated"
    MODE_PRODUCTION: bool = mode == "production"
    
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    SECRET_KEY: str = secrets.token_urlsafe(32)

    PROTOCOL: str
    SERVER_NAME: str
    BASE_PATH: str
    COMPLETE_SERVER_NAME: AnyHttpUrl = os.getenv("PROTOCOL") + os.getenv("SERVER_NAME") + os.getenv("BASE_PATH")

    MONGODB_URL: str
    MONGODB_DATABASE: str
    COLLECTION_NAME: str

    ETHERPAD_API_KEY: str
    ETHERPAD_HOST: str
    ETHERPAD_PORT: int
    ETHERPAD_SERVICE: str = os.getenv("ETHERPAD_HOST") + ":" + os.getenv("ETHERPAD_PORT")


    class Config:
        case_sensitive = True


settings = Settings()
