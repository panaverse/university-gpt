from fastapi import APIRouter, Depends, Query
from typing import Annotated

from api.core.database import get_session, AsyncSession
from api.quiz.topic.crud import (create_topic, read_topics, get_topic_by_id, get_topic_by_name, update_topic, delete_topic,
                                 create_new_content, read_content_for_topic, get_content_by_id, update_content, delete_content)

from api.quiz.topic.models import TopicCreate, TopicResponse, TopicUpdate, TopicResponseWithContent, ContentCreate, ContentResponse, ContentUpdate
from api.core.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)

# Create new Recursive Topic
@router.post("", response_model=TopicResponseWithContent)
async def create_a_topic(topic: TopicCreate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Create a new recursive topic.

    Args:
        topic (TopicCreate): The topic data to create.
       db (optional) : Database Dependency Injection.

    Returns:
        TopicResponse: The created topic.
    """
    logger.info("%s.create_a_topic: %s", __name__, topic)
    return await create_topic(topic=topic, db=db)

# Get all Topics
@router.get("", response_model=list[TopicResponse])
async def get_topics(
    db: Annotated[AsyncSession, Depends(get_session)],
    offset: int = Query(default=0, lte=10),
    limit: int = Query(default=10, lte=100),
):
    """
    Get all topics.

    Args:
        offset (int, optional): The offset for pagination. Defaults to 0.
        limit (int, optional): The limit for pagination. Defaults to 100.
       db (optional) : Database Dependency Injection.

    Returns:
        list[TopicResponse]: The list of topics.
    """
    logger.info("%s.get_topics: triggered", __name__)
    return await read_topics(offset=offset, limit=limit, db=db)

# Get a Topic by ID
@router.get("/{topic_id}", response_model=TopicResponse)
async def call_get_topic_by_id(topic_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Get a topic by ID.

    Args:
        topic_id (int): The ID of the topic.
       db (optional) : Database Dependency Injection.

    Returns:
        TopicResponse: The topic with the specified ID.
    """
    logger.info("%s.get_topic_by_id: %s", __name__, topic_id)
    return await get_topic_by_id(id=topic_id, db=db)

# Get a Topic by Name
@router.get("/name/{name}", response_model=TopicResponse)
async def call_get_topic_by_name(name: str, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Get a topic by name.

    Args:
        name (str): The name of the topic.
       db (optional) : Database Dependency Injection.

    Returns:
        TopicResponse: The topic with the specified name.
    """
    logger.info("%s.get_topic_by_name: %s", __name__, name)
    return await get_topic_by_name(name=name, db=db)

# Update a Topic by ID
@router.patch("/{topic_id}", response_model=TopicResponse)
async def update_topic_by_id(topic_id: int, topic: TopicUpdate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Update a topic by ID.

    Args:
        topic_id (int): The ID of the topic to update.
        topic (TopicUpdate): The updated topic data.
       db (optional) : Database Dependency Injection.

    Returns:
        TopicResponse: The updated topic.
    """
    logger.info("%s.update_topic_by_id: %s", __name__, topic_id)
    return await update_topic(id=topic_id, topic=topic, db=db)

# Delete a Topic by ID
@router.delete("/{topic_id}")
async def delete_topic_by_id(topic_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Delete a topic by ID.

    Args:
        topic_id (int): The ID of the topic to delete.
        db (optional) : Database Dependency Injection.
    """
    logger.info("%s.delete_topic_by_id: %s", __name__, topic_id)
    return await delete_topic(id=topic_id, db=db)


# Create new Content for a Topic
@router.post("/content", response_model=ContentResponse)
async def create_content_for_topic( content: ContentCreate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Create a new content for a topic.

    Args:
        topic_id (int): The ID of the topic.
        content (ContentCreate): The content data to create.
       db (optional) : Database Dependency Injection.

    Returns:
        ContentResponse: The created content.
    """
    logger.info("%s.create_content_for_topic: %s", __name__, content)
    return await create_new_content(content=content, db=db)

# Get all Content for a Topic
@router.get("/{topic_id}/content", response_model=list[ContentResponse])
async def get_content_for_topic(topic_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Get all content for a topic.

    Args:
        topic_id (int): The ID of the topic.
       db (optional) : Database Dependency Injection.

    Returns:
        list[ContentResponse]: The list of content for the topic.
    """
    logger.info("%s.get_content_for_topic: %s", __name__, topic_id)
    return await read_content_for_topic(topic_id=topic_id, db=db)

# Get a Content by ID
@router.get("/{topic_id}/content/{content_id}", response_model=ContentResponse)
async def call_get_content_by_id(topic_id: int, content_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Get a content by ID.

    Args:
        topic_id (int): The ID of the topic.
        content_id (int): The ID of the content.
       db (optional) : Database Dependency Injection.

    Returns:
        ContentResponse: The content with the specified ID.
    """
    logger.info("%s.get_content_by_id: %s", __name__, content_id)
    return await get_content_by_id(topic_id=topic_id, content_id=content_id, db=db)

# Update a Content by ID
@router.patch("/content/{content_id}", response_model=ContentResponse)
async def update_content_by_id(content_id: int, content: ContentUpdate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Update a content by ID.

    Args:
        topic_id (int): The ID of the topic.
        content_id (int): The ID of the content to update.
        content (ContentUpdate): The updated content data.
       db (optional) : Database Dependency Injection.

    Returns:
        ContentResponse: The updated content.
    """
    logger.info("%s.update_content_by_id: %s", __name__, content_id)
    return await update_content(id=content_id, content=content, db=db)

# Delete a Content by ID
@router.delete("/content/{content_id}")
async def delete_content_by_id(content_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Delete a content by ID.

    Args:
        topic_id (int): The ID of the topic.
        content_id (int): The ID of the content to delete.
       db (optional) : Database Dependency Injection.
    """
    logger.info("%s.delete_content_by_id: %s", __name__, content_id)
    return await delete_content(id=content_id, db=db)