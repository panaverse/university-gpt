from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
# from sqlalchemy.orm import sessionmaker

from sqlmodel.ext.asyncio.session import AsyncSession
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

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# @asynccontextmanager #TODO: Do we need this?
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session


# AsyncSessionLocal = sessionmaker(
#         bind=async_engine,
#         class_=AsyncSession,
#         expire_on_commit=False,
#         autoflush=False,
#         autocommit=False,
#     )

# # @asynccontextmanager
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         yield session
