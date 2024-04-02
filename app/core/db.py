from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

# import sessionmaker from sqlalchemy
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession
from collections.abc import AsyncGenerator
from app.core import settings

async_conn_string: str = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+asyncpg"
)

# Create an asynchronous engine for the database
async_engine = create_async_engine(
    url=async_conn_string,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=300,
)


# @asynccontextmanager #TODO: Do we need this? It was causing errors for db.execute
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async with async_session() as session:
        yield session
