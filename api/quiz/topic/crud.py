from fastapi import HTTPException, status
from sqlmodel import select, and_

from api.core.database import AsyncSession
from api.quiz.topic.models import Topic, TopicCreate, TopicUpdate, Content, ContentCreate, ContentUpdate

# Create a new topic [Recursive Topics]
async def create_topic(topic: TopicCreate, db: AsyncSession ):
    """
    Create a new topic or subtopic in the database.

    Args:
        topic (TopicCreate): The topic data to be created.
        db (optional) : Database Dependency Injection.

    Returns:
        Topic: The created topic.

    Raises:
        None
    """

    if topic.contents:
        topic.contents = [Content.model_validate(content) for content in topic.contents]

    topic_to_db = Topic.model_validate(topic)


    db.add(topic_to_db)
    await db.commit()
    db.refresh(topic_to_db)
    print(f"TRANSFORMATION CONTENT in Topic TO DB: {topic_to_db.contents}")
    return topic_to_db

# Get all topics
async def read_topics(offset: int, limit: int, db: AsyncSession ):
    """
    Retrieve a list of topics from the database.

    Args:
        offset (int): The number of topics to skip before starting to return results.
        limit (int): The maximum number of topics to return.
        db (optional) : Database Dependency Injection.

    Returns:
        List[Topic]: A list of Topic objects.

    """
    result = await db.execute(select(Topic).offset(offset).limit(limit))
    topics = result.scalars().all()
    return topics

# Get a Topic by Name
async def get_topic_by_name(name: str, db: AsyncSession ):
    result = await db.execute(select(Topic).where(Topic.title == name))
    topic = result.scalars().first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic

# Get a Topic by ID
async def get_topic_by_id(id: int, db: AsyncSession ):
    """
    Retrieve a topic by its ID.

    Args:
        id (int): The ID of the topic to retrieve.
        db (optional) : Database Dependency Injection.

    Returns:
        Topic: The retrieved topic.

    Raises:
        HTTPException: If the topic with the given ID is not found.
    """
    topic = await db.get(Topic, id)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic

# Update a Topic by ID
async def update_topic(id: int, topic: TopicUpdate, db: AsyncSession ):
    """
    Update a topic in the database.

    Args:
        id (int): The ID of the topic to update.
        topic (TopicUpdate): The updated topic data.
        db (optional) : Database Dependency Injection.

    Returns:
        Topic: The updated topic.
        
    Raises:
        HTTPException: If the topic with the given ID is not found.
    """
    topic_to_update = await db.get(Topic, id)
    if not topic_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    topic_data = topic.model_dump(exclude_unset=True)
    for key, value in topic_data.items():
        setattr(topic_to_update, key, value)
    db.add(topic_to_update)
    await db.commit()
    await db.refresh(topic_to_update)
    return topic_to_update

# Delete a Topic by ID
async def delete_topic(id: int, db: AsyncSession ):
    """
    Deletes a topic from the database based on the provided ID.

    Args:
        id (int): The ID of the topic to be deleted.
        db (optional) : Database Dependency Injection.

    Raises:
        HTTPException: If the topic with the provided ID is not found.

    Returns:
        dict: A dictionary with a message indicating the successful deletion of the topic.
    """
    try:
        topic = await db.get(Topic, id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
        await db.delete(topic)
        await db.commit()
        return {"message": "Topic deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting topic: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting topic")
    
# Create a new content for a topic
async def create_new_content(content: ContentCreate, db: AsyncSession ):
    """
    Create a new content for a topic in the database.

    Args:
        content (ContentCreate): The content data to be created.
        db (optional) : Database Dependency Injection.

    Returns:
        Content: The created content.

    Raises:
        None
    """
    content_to_db = Content.model_validate(content)
    db.add(content_to_db)
    await db.commit()
    db.refresh(content_to_db)
    return content_to_db

# Get all content for a topic
async def read_content_for_topic(topic_id: int, db: AsyncSession ):
    """
    Retrieve a list of content for a topic from the database.

    Args:
        topic_id (int): The ID of the topic to retrieve content for.
        db (optional) : Database Dependency Injection.

    Returns:
        List[Content]: A list of Content objects.

    """
    result = await db.execute(select(Content).where(Content.topic_id == topic_id))
    content = result.scalars().all()
    return content

# Get a Content by ID
async def get_content_by_id(topic_id: int, content_id: int, db: AsyncSession ):
    """
    Retrieve a content by its ID.

    Args:
        topic_id (int): The ID of the topic for which content to retrieve.
        content_id (int): The ID of the content to retrieve.
        db (optional) : Database Dependency Injection.

    Returns:
        Content: The retrieved content.

    Raises:
        HTTPException: If the content with the given ID is not found.
    """

    result = await db.execute(select(Content).where(and_(Content.topic_id == topic_id, Content.id == content_id)))
    content = result.scalars().one()

    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return content

# Update a Content by ID
async def update_content(id: int, content: ContentUpdate, db: AsyncSession ):
    """
    Update a content in the database.

    Args:
        id (int): The ID of the content to update.
        content (ContentUpdate): The updated content data.
        db (optional) : Database Dependency Injection.

    Returns:
        Content: The updated content.
        
    Raises:
        HTTPException: If the content with the given ID is not found.
    """
    content_to_update = await db.get(Content, id)
    if not content_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    content_data = content.model_dump(exclude_unset=True)
    for key, value in content_data.items():
        setattr(content_to_update, key, value)
    db.add(content_to_update)
    await db.commit()
    db.refresh(content_to_update)
    return content_to_update


# Delete a Content by ID
async def delete_content(id: int, db: AsyncSession ):
    """
    Deletes a content from the database based on the provided ID.

    Args:
        id (int): The ID of the content to be deleted.
        db (optional) : Database Dependency Injection.

    Raises:
        HTTPException: If the content with the provided ID is not found.

    Returns:
        dict: A dictionary with a message indicating the successful deletion of the content.
    """
    try:
        content = await db.get(Content, id)
        if not content:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
        await db.delete(content)
        await db.commit()
        return {"message": "Content deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting content: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting content")