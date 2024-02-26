from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
from os import getenv
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import AsyncIterator

# Load environment variables
load_dotenv(find_dotenv())

# Database connection string
DATABASE_URL = getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create an asynchronous engine for the database
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=3600,
)


# Ayschronous Context manager for handling database sessions
# @asynccontextmanager #TODO: Do we need this? It was causing errors for db.execute
async def get_session() -> AsyncIterator[AsyncSession]:
    async_session = async_sessionmaker(engine, class_ = AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session