import pytest
from app.pre_start_tests import TestAsyncSessionLocal


@pytest.fixture(scope="class")
async def async_db_session():
    """Fixture to provide a database session for tests, automatically handling context."""
    async with TestAsyncSessionLocal() as session:
        yield session
