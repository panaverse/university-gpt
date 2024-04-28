from starlette.config import Config
from starlette.datastructures import Secret

from app.core.utils import parse_cors

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

PROJECT_NAME: str = config("PROJECT_NAME", cast=str)
DESCRIPTION: str = config(
    "DESCRIPTION", default="API Service for Quiz GPT GenAI", cast=str
)

ENV: str = config("ENV", default="development", cast=str)
VERSION: str = "0.1"

DATABASE_URL: Secret = config("DATABASE_URL", cast=Secret)
TEST_DATABASE_URL: Secret = config("TEST_DATABASE_URL", cast=Secret)

BACKEND_CORS_ORIGINS_STR: str = config("BACKEND_CORS_ORIGINS", default="*", cast=str)
BACKEND_CORS_ORIGINS: list[str] | str = parse_cors(BACKEND_CORS_ORIGINS_STR)

API_V1_STR="/api/v1"

EDUCATIONAL_PROGRAM_URL = config("EDUCATIONAL_PROGRAM_URL", cast=str)
QUIZ_ENGINE_API_URL = config("QUIZ_ENGINE_API_URL", cast=str)