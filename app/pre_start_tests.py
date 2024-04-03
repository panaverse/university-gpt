import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import SQLModel, create_engine
from app.core import settings
from app.init_data import init_db
from app.core.db import AsyncSession
from app.models import *
from app.core.config import logger_config
from sqlalchemy.pool import NullPool

logger = logger_config(__name__)

async_conn_string: str = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+asyncpg"
)

# Create an asynchronous engine for the database
test_async_engine = create_async_engine(
    url=async_conn_string,
    echo=True,
    # future=True,
    # pool_size=20,
    # max_overflow=20,
    # pool_recycle=3600,
    poolclass=NullPool,  # for Pytesting
)

TestAsyncSessionLocal = async_sessionmaker(
    bind=test_async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def init_test_db_once():
    logger.info("Creating Tables in Test Database")
    SQLModel.metadata.create_all(
        create_engine(str(settings.TEST_DATABASE_URL), echo=True)
    )
    logger.info("Test Database Tables Created")

    logger.info("Initializing Test Database")
    await init_db(async_session=TestAsyncSessionLocal)
    logger.info("Test Database Initialized")
    logger.info("Reading Test Files!")


if __name__ == "__main__":
    asyncio.run(init_test_db_once())
