from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker

from fastapi import HTTPException

import pytest
import sys
import os
sys.path.append(os.getcwd())

from app.quiz.topic.crud import (create_topic, read_topics, read_topic_by_id, update_topic, delete_topic,
                                 create_new_content, read_content_for_topic, get_content_by_id, update_content, delete_content)
from app.quiz.topic.models import TopicCreate, TopicUpdate, ContentCreate, ContentUpdate

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

@pytest.fixture(scope="class")
async def async_db_session():
    """Fixture to provide a database session for tests, automatically handling context."""
    async_session = async_sessionmaker(engine, class_ = AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

# A Fixture to Use Once Created Topic for Get, Patch, Delete
@pytest.fixture(scope="class")
async def new_topic(async_db_session):
    async for session in async_db_session:
        title = "TS OOP"
        description = "Learn OOPS in Typescript 5.0+"
        topic_data = TopicCreate(title=title, description=description)
        new_topic_created = await create_topic(topic=topic_data, db=session)
        yield new_topic_created
        # We will delete Topic after in the last test case instead
        await delete_topic(id=new_topic.id, db=session)

class TestTopicCRUD:
    title= "TS OOP"
    description= "Learn OOPS in Typescript 5.0+"

    # @pytest.mark.asyncio
    # async def test_read_topics(self, async_db_session):
    #     async for session in async_db_session:
    #         topics = await read_topics(offset=0, limit=10, db=session)
    #         assert topics is not None
    #         assert len(topics) >= 0

    @pytest.mark.asyncio
    async def test_get_topic_by_id(self, async_db_session, new_topic):
        async for session in async_db_session:
            async for topic in new_topic:
                fetched_topic = await read_topic_by_id(id=topic.id, db=session)
                assert fetched_topic is not None
                assert fetched_topic.title == self.title
                assert fetched_topic.description == self.description

    @pytest.mark.asyncio
    async def test_update_topic(self, async_db_session, new_topic):
        async for session in async_db_session:
            new_title = "OOP in Python"
            new_description = "Learn OOPS in Python 3.9+"
            topic_update = TopicUpdate(title=new_title, description=new_description)
            async for topic in new_topic:
                updated_topic = await update_topic(id=topic.id, topic=topic_update, db=session)
                assert updated_topic is not None
                assert updated_topic.title == new_title
                assert updated_topic.description == new_description

    # @pytest.mark.asyncio
    # async def test_delete_topic(self, async_db_session, new_topic):
    #     async for session in async_db_session:
    #         async for topic in new_topic:
    #             await delete_topic(id=topic.id, db=session)
    #             deleted_topic = await get_topic_by_id(id=topic.id, db=session)
    #             assert deleted_topic is None

    # More Edge Cases
    # ValueError for create_topic
    @pytest.mark.asyncio
    async def test_create_topic_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                topic = TopicCreate(description="")
                await create_topic(topic=topic, db=session)

    # ValueError for get_topic_by_name
    @pytest.mark.asyncio
    async def test_get_topic_by_name_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                await get_topic_by_name(name="", db=session)

    # ValueError for get_topic_by_id
    @pytest.mark.asyncio
    async def test_get_topic_by_id_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                await get_topic_by_id(id=0, db=session)

    # ValueError for update_topic
    @pytest.mark.asyncio
    async def test_update_topic_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                topic = TopicUpdate(title="", description="")
                await update_topic(id=9999, topic=topic, db=session)

    # HttpException for delete_topic
    @pytest.mark.asyncio
    async def test_delete_topic_http_exception(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(HTTPException):
                await delete_topic(id=9999, db=session)


@pytest.fixture(scope="class")
async def new_mock_content(async_db_session, new_topic):
    async for session in async_db_session:
        async for topic in new_topic:
            content_data = ContentCreate(topic_id=topic.id , content_text="Learn about classes in OOP")
            new_content = await create_new_content(content=content_data, db=session)
            yield new_content
            
            await delete_content(id=new_content.id, db=session)

class TestContentCrud:
    content_text= "Learn OOPS in Typescript 5.0+"

    # Test read_content_for_topic
    @pytest.mark.asyncio
    async def test_read_content_for_topic(self, async_db_session, new_mock_content):
        async for session in async_db_session:
            async for mock_content in new_mock_content:
                content = await read_content_for_topic(topic_id=mock_content.topic_id, db=session)
                assert content is not None
                assert len(content) >= 0
    
    #  Pass Non Existing Topic ID
    @pytest.mark.asyncio
    async def test_read_content_for_topic_non_existing_topic_id(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(HTTPException):
                await read_content_for_topic(topic_id=9999, db=session)

    # Test get_content_by_id
    @pytest.mark.asyncio
    async def test_get_content_by_id(self, async_db_session, new_mock_content):
        async for session in async_db_session:
            async for mock_content in new_mock_content:
                content = await get_content_by_id(topic_id=mock_content.topic_id, content_id=mock_content.id, db=session)
                assert content is not None
                assert content.content_text == self.content_text

    # Non Existing Topic ID
    @pytest.mark.asyncio
    async def test_get_content_by_id_non_existing_topic_id(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(HTTPException):
                await get_content_by_id(topic_id=9999, content_id=9999, db=session)

    #  update_content
    @pytest.mark.asyncio
    async def test_update_content(self, async_db_session, new_mock_content):
        async for session in async_db_session:
            content = ContentUpdate(content_text="New Classes")
            async for mock_content in new_mock_content:
                updated_content = await update_content(id=mock_content.id, content=content, db=session)
                assert updated_content is not None
                assert updated_content.content_text == "New Classes"

    # Non Existing Topic ID
    @pytest.mark.asyncio
    async def test_update_content_non_existing_topic_id(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(HTTPException):
                content = ContentUpdate(content_text="New Classes")
                await update_content(id=9999, content=content, db=session)


