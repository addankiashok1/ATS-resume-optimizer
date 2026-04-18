import os
from typing import List
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    JWT_SECRET_KEY: str = Field(..., min_length=1)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GOOGLE_CLIENT_ID: str
    LINKEDIN_CLIENT_ID: str
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    model_config = {
        "env_file": os.path.join(os.path.dirname(__file__), "../../.env"),
        "env_file_encoding": "utf-8",
    }


settings = Settings()
