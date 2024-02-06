from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.config import Settings
# from api.core.database import create_db_and_tables
from api.quiz import api as public_api
from api.core.utils.logger import logger_config

logger = logger_config(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create_db_and_tables()

    logger.info("startup: triggered")

    yield

    logger.info("shutdown: triggered")


def create_app(settings: Settings):
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/",
        description=settings.DESCRIPTION,
        lifespan=lifespan,
        servers=[{"url": "http://localhost:8080", "description": "Development Server"}]
    )

    app.include_router(public_api)

    return app
