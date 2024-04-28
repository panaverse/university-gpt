from fastapi import APIRouter, Query, HTTPException, status
from app.api.deps import DBSessionDep

from app.crud.content_crud import content_crud
from app.models.content_models import ContentCreate, ContentResponse, ContentUpdate
from app.core.config import logger_config

router = APIRouter()

logger = logger_config(__name__)


# Create new Content for a Topic
@router.post("/", response_model=ContentResponse)
def create_content_for_topic(content: ContentCreate, db: DBSessionDep):
    """
    Create a new content for a topic.

    Args:
        content (ContentCreate): The content data to create that is topic_id and content_text.

    Returns:
        ContentResponse: The created content.
    """
    logger.info("%s.create_content_for_topic: %s", __name__, content)
    try:
        return content_crud.create_new_content(content=content, db=db)
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as ex:
        logger.error(f"Unexpected error occurred while creating content: {ex}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )


# Get all Content for a Topic
@router.get("/{topic_id}/content", response_model=list[ContentResponse])
def get_content_for_topic(topic_id: int, db: DBSessionDep):
    """
    Get all content for a topic.

    Args:
        topic_id (int): The ID of the topic.

    Returns:
        list[ContentResponse]: The list of content for the topic.
    """
    logger.info("%s.get_content_for_topic: %s", __name__, topic_id)
    try:
        all_contents = content_crud.read_content_for_topic(
            topic_id=topic_id, db=db
        )
        return all_contents

    except HTTPException as http_err:
        logger.error(f"Error retrieving content: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error retrieving content: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve content.")


# Get a Content by ID
@router.get("/{topic_id}/content/{content_id}", response_model=ContentResponse)
def call_get_content_by_id(topic_id: int, content_id: int, db: DBSessionDep):
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
    try:
        return content_crud.get_content_by_id(
            topic_id=topic_id, content_id=content_id, db=db
        )
    except HTTPException as http_err:
        logger.error(f"Error retrieving content: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error retrieving content: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve content.")


# Update a Content by ID
@router.patch("/{content_id}", response_model=ContentResponse)
def update_content_by_id(
    content_id: int, content: ContentUpdate, db: DBSessionDep
):
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
    try:
        return content_crud.update_content(id=content_id, content=content, db=db)
    except HTTPException as http_err:
        logger.error(f"Error updating content: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error updating content: {e}")
        raise HTTPException(status_code=500, detail="Failed to update content.")


# Delete a Content by ID


@router.delete("/{content_id}")
def delete_content_by_id(content_id: int, db: DBSessionDep):
    """
    Delete a content by ID.

    Args:
        topic_id (int): The ID of the topic.
        content_id (int): The ID of the content to delete.
       db (optional) : Database Dependency Injection.
    """
    logger.info("%s.delete_content_by_id: %s", __name__, content_id)
    return content_crud.delete_content(id=content_id, db=db)
