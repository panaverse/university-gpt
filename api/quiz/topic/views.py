from fastapi import APIRouter, Depends, Query
from typing import Annotated

from api.core.database import get_session, AsyncSession
from api.quiz.topic.crud import create_topic, read_topics, get_topic_by_id, get_topic_by_name, update_topic, delete_topic

from api.quiz.topic.models import TopicCreate, TopicResponse, TopicUpdate
from api.core.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)

# Create new Recursive Topic
@router.post("", response_model=TopicResponse)
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
