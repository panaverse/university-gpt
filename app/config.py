import os
import secrets
from typing import Literal

from pydantic_settings import BaseSettings

from dotenv import load_dotenv, find_dotenv

_: bool = load_dotenv(find_dotenv())


class Settings(BaseSettings):
    PROJECT_NAME: str = f"Quiz GPT API - {os.getenv('ENV', 'development').capitalize()}"
    DESCRIPTION: str = "Quiz GPT GenAI API Service"
    ENV: Literal["development", "staging", "production"] = "development"
    VERSION: str = "0.1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URI: str = os.environ.get("DATABASE_URL", "")
    API_USERNAME: str = os.environ.get("API_USER", "panaverse")
    API_PASSWORD: str = os.environ.get("API_PASSW", "panaverse")

    class Config:
        case_sensitive = True


settings = Settings()


class TestSettings(Settings):
    class Config:
        case_sensitive = True


test_settings = TestSettings()
