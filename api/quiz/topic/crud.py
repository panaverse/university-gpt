from fastapi import HTTPException, status
from sqlmodel import select, and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import selectinload

from api.core.database import AsyncSession
from api.quiz.topic.models import Topic, TopicCreate, TopicUpdate, Content, ContentCreate, ContentUpdate
from api.core.utils.logger import logger_config

logger = logger_config(__name__)

# Create a new topic [Recursive Topics]
async def create_topic(topic: TopicCreate, db: AsyncSession) -> Topic:
    """
    Create a new topic or subtopic in the database.

    Args:
        topic (TopicCreate): The topic data to be created.
        db (AsyncSession): The database session.

    Returns:
        Topic: The created topic.

    Raises:
        ValueError: For data integrity issues.
        SQLAlchemyError: For database operation errors.
        Exception: For unexpected errors.
    """
    try:
        # Validate and add associated contents if present
        if topic.contents:
            topic.contents = [Content.model_validate(content) for content in topic.contents]

        # Transform TopicCreate schema into Topic model instance
        topic_to_db = Topic.model_validate(topic)

        # Add the new topic to the database and commit the transaction
        db.add(topic_to_db)
        await db.commit()
        db.refresh(topic_to_db)
        
        return topic_to_db

    except IntegrityError as e:
        await db.rollback()  # Ensure rollback is awaited
        logger.error(f"CREATE_TOPIC: An integrity error occurred while creating the topic: {e}")
        raise ValueError("Data integrity issue.") from e

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"CREATE_TOPIC: A database error occurred while creating the topic: {e}")
        raise SQLAlchemyError("Database operation failed.") from e

    except Exception as e:
        await db.rollback()
        logger.error(f"CREATE_TOPIC: An unexpected error occurred: {e}")
        raise Exception("An unexpected error occurred.") from e

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
    
    Raises:
        HTTPException: If no topics are found or for other HTTP-related errors.
        SQLAlchemyError: For database operation errors.
        Exception: For unexpected errors.

    """
    try:
        result = await db.execute(select(Topic).offset(offset).limit(limit))
        topics = result.scalars().all()
        if not topics:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No topics found")
        return topics
    except HTTPException as e:
        await db.rollback()
        logger.error(f"READ_TOPICS: No topics found: {e}")
        raise e  # Re-raise the HTTPException with the original status code and detail
    except SQLAlchemyError as e:
        await db.rollback()  # Ensure rollback is awaited
        logger.error(f"READ_TOPICS: A database error occurred while retrieving topics: {e}")
        raise SQLAlchemyError("Database operation failed.") from e
    except Exception as e:
        await db.rollback()  # Ensure rollback is awaited
        logger.error(f"READ_TOPICS: An unexpected error occurred: {e}")
        raise Exception("An unexpected error occurred.") from e

# Get a Topic by ID
async def read_topic_by_id(id: int, db: AsyncSession ):
    """
    Retrieve a topic by its ID.

    Args:
        id (int): The ID of the topic to retrieve.
        db (optional) : Database Dependency Injection.

    Returns:
        Topic: The retrieved topic.

    Raises:
       HTTPException
    """
    try:
        # topic = await db.get(Topic, id)
        result = await db.execute(select(Topic).options(selectinload(Topic.contents)).where(Topic.id == id))
        topic = result.scalars().one()
        if not topic:
            raise ValueError("Topic not found")
        return topic
    
    except ValueError as e:
        await db.rollback()  # Ensure rollback is awaited
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except SQLAlchemyError as e:
        await db.rollback()  # Ensure rollback is awaited
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

    except Exception as e:
        await db.rollback()  # Ensure rollback is awaited
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


# Read Topic & all its Subtopics
async def read_topic_and_subtopics(id: int, db: AsyncSession ):
    try:
        topic_result = await db.execute(select(Topic).options(selectinload(Topic.children_topics), selectinload(Topic.parent_topic)).where(Topic.id == id))
        topic = topic_result.scalars().first()

        if not topic:
            raise ValueError(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

        parent_topic_id = topic.parent_topic.id if topic.parent_topic else None
        children_topic_ids = [child.id for child in topic.children_topics]
        children_topics = [child for child in topic.children_topics]

        return {
            "topic_id": topic.id,
            "title": topic.title,
            "description": topic.description,
            "parent_topic_id": parent_topic_id,
            "children_topic_ids": children_topic_ids,
            "children_topic": children_topics
        }

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

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
        ValueError: If the topic with the given ID is not found.
    """
    try:
        topic_to_update = await db.get(Topic, id)
        if not topic_to_update:
            raise ValueError("Topic not found")
        topic_data = topic.model_dump(exclude_unset=True)
        for key, value in topic_data.items():
            setattr(topic_to_update, key, value)
        db.add(topic_to_update)
        await db.commit()
        await db.refresh(topic_to_update)
        return topic_to_update
    except ValueError:
        await db.rollback()
        logger.error(f"UPDATE_TOPIC: Topic not found")
        raise ValueError("Topic not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"UPDATE_TOPIC: Error updating topic: {str(e)}")
        raise SQLAlchemyError("Error updating topic")
    except Exception as e:
        await db.rollback()
        logger.error(f"UPDATE_TOPIC: Error updating topic: {str(e)}")
        raise Exception("Error updating topic")

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
        await db.rollback()
        raise e
    except Exception as e:
        await db.rollback()
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
        HTTPException: For specific handled errors such as IntegrityError.
        Exception: For unexpected errors.
    """
    try:
        content_to_db = Content.model_validate(content)
        db.add(content_to_db)
        await db.commit()
        await db.refresh(content_to_db)
        return content_to_db
    except IntegrityError as e:
        await db.rollback()
        # Logging the error might help in debugging, ensure logger is configured properly
        logger.error(f"CREATE_NEW_CONTENT: Integrity error occurred: {e}")
        # Raising HTTPException to inform the caller about the specific issue
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Foreign key constraint failed, the topic might not exist."
        ) from e
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"CREATE_NEW_CONTENT: Database operation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed."
        ) from e
    except Exception as e:
        await db.rollback()
        logger.error(f"CREATE_NEW_CONTENT: Unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        ) from e

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
    try:
        result = await db.execute(select(Content).where(Content.topic_id == topic_id))
        content = result.scalars().all()
        if not content:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No content found")
        return content
    except HTTPException as e:
        await db.rollback()
        logger.error(f"READ_TOPICS: No topics found: {e}")
        raise e  # Re-raise the HTTPException with the original status code and detail
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"READ_TOPICS: Integrity error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Foreign key constraint failed, the topic might not exist."
        ) from e
    except SQLAlchemyError as e:
        await db.rollback()  # Ensure rollback is awaited
        logger.error(f"READ_TOPICS: A database error occurred while retrieving topics: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database operation failed.") from e
    except Exception as e:
        await db.rollback()  # Ensure rollback is awaited
        logger.error(f"READ_TOPICS: An unexpected error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.") from e


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

    try:
        result = await db.execute(select(Content).where(and_(Content.topic_id == topic_id, Content.id == content_id)))
        content = result.scalars().one()

        if not content:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
        return content
    
    except HTTPException as e:
        await db.rollback()
        logger.error(f"GET_CONTENT_BY_ID: Content not found: {e}")
        raise e
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"GET_CONTENT_BY_ID: Integrity error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Foreign key constraint failed, the topic might not exist.")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"GET_CONTENT_BY_ID: Database operation failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database operation failed.")
    except Exception as e:
        await db.rollback()
        logger.error(f"GET_CONTENT_BY_ID: Unexpected error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


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
    try:
        content_to_update = await db.get(Content, id)
        if not content_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
        content_data = content.model_dump(exclude_unset=True)
        for key, value in content_data.items():
            setattr(content_to_update, key, value)
        db.add(content_to_update)
        await db.commit()
        await db.refresh(content_to_update)
        return content_to_update
    
    except HTTPException as e:
        await db.rollback()
        logger.error(f"UPDATE_CONTENT: Content not found: {e}")
        raise e
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"UPDATE_CONTENT: Integrity error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Foreign key constraint failed, the topic might not exist.")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"UPDATE_CONTENT: Database operation failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database operation failed.")
    except Exception as e:
        await db.rollback()
        logger.error(f"UPDATE_CONTENT: Unexpected error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


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
            raise ValueError("Content not found")
        await db.delete(content)
        await db.commit()
        return {"message": "Content deleted successfully"}
    except ValueError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    except Exception as e:
        await db.rollback()
        print(f"Error deleting content: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting content")