from httpx import AsyncClient

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker

import pytest
import sys
import os
sys.path.append(os.getcwd())

from asgi import api
from api.core.database import get_session

# Load environment variables
load_dotenv(find_dotenv())

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create an asynchronous engine for the database
engine = create_async_engine(DATABASE_URL, echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=3600)

async def async_db_session():
    """Fixture to provide a database session for tests, automatically handling context."""
    async_session = async_sessionmaker(engine, class_ = AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

# api.dependency_overrides[get_session] = async_db_session
# client = TestClient(api)


@pytest.mark.asyncio
async def test_question_creation_deletion():
    api.dependency_overrides[get_session] = async_db_session
    async with AsyncClient(app=api, base_url="http://localhost:8080") as ac:

        # Create a topic
        response = await ac.post("/quiz/api/v1/topics", json={"title": "Test Topic", "description": "Test Description"})
        topic_id = response.json()['id']

       # Create a question
        response = await ac.post("/quiz/api/v1/questions", json={
            "difficulty": "easy",
            "is_verified": True,
            "points": 1,
            "question_text": "What is a common cause of syntax errors in TypeScript?",
            "question_type": "single_select_mcq",
            "topic_id": topic_id
            })
        assert response.status_code == 200
        assert response.json()["question_text"] == "What is a common cause of syntax errors in TypeScript?"

        
        await ac.delete(f"/quiz/api/v1/questions/{response.json()['id']}")
        await ac.delete(f"/quiz/api/v1/topics/{topic_id}")
