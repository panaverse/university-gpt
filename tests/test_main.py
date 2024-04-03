import pytest
from httpx import AsyncClient
from typing import AsyncGenerator

from app.core import settings
from app.main import app
from app.core.db import get_async_session
from app.pre_start_tests import TestAsyncSessionLocal


# @pytest.fixture(scope="session", autouse=True)
async def override_session():
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_async_session] = override_session
    async with AsyncClient(app=app, base_url=settings.DEV_URL) as client:
        yield client


@pytest.mark.asyncio
async def test_root(test_client):
    async for client in test_client:
        response = await client.get("/api")
    assert response is not None
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
