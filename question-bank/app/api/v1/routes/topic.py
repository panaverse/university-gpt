from fastapi import APIRouter, Query, HTTPException
from app.api.deps import DBSessionDep, CourseDep
from app.crud.topic_crud import topic_crud
from app.models.topic_models import (
    TopicCreate,
    TopicResponse,
    TopicUpdate,
    TopicResponseWithContent,
    PaginatedTopicRead
)
from app.core.config import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.post("", response_model=TopicResponseWithContent)
def create_new_topic(topic: TopicCreate, db: DBSessionDep, course: CourseDep):
    """
    Create a new recursive topic.

    Args:
        topic (TopicCreate): The topic data to create.

    Returns:
        TopicResponse: The created topic.

    Raises:
        HTTPException: If an error occurs while creating the topic.
    """
    logger.info("%s.create_a_topic: %s", __name__, topic)
    try:
        print("Verifing if Content Id is Valid", course)
        created_topic = topic_crud.create_topic(topic=topic, db=db)
        return created_topic
    except (
        ValueError
    ) as e:  # Catching the custom ValueError raised from CRUD operations
        logger.error(f"Error creating topic: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as httperr:
        logger.error(f"Error creating topic: {httperr}")
        raise httperr
    except Exception as e:  # Catching any unexpected errors
        logger.error(f"Unexpected error creating topic: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("", response_model=PaginatedTopicRead)
def get_all_topics(
    db: DBSessionDep,
    page: int = Query(1, description="Page number", ge=1),
    per_page: int = Query(10, description="Items per page", ge=1, le=100)
):
    """
    Get all topics.

    Args:
        offset (int, optional): The offset for pagination. Defaults to 0.
        limit (int, optional): The limit for pagination. Defaults to 100.

    Returns:
        PaginatedTopicRead: The list of topics paginated.

    Raises:
        HTTPException: If an error occurs while retrieving topics.
    """
    logger.info("%s.get_topics: triggered", __name__)
    try:
        # topics = topic_crud.read_topics(offset=offset, limit=limit, db=db)
        # return topics
                # Calculate the offset to skip the appropriate number of items
        offset = (page - 1) * per_page
        all_records = topic_crud.read_topics(db=db, offset=offset, per_page=per_page)
        count_recs = topic_crud.count_records(db=db)

        # Calculate next and previous page URLs
        next_page = f"?page={page + 1}&per_page={per_page}" if len(all_records) == per_page else None
        previous_page = f"?page={page - 1}&per_page={per_page}" if page > 1 else None

        # Return data in paginated format
        paginated_data = {"count": count_recs, "next": next_page, "previous": previous_page, "results": all_records}

        return paginated_data
    
    except HTTPException as http_err:
        logger.error(f"Error retrieving topics: {http_err}")
        raise http_err  # Re-raise the HTTPException with the original status code and detail
    except Exception as e:
        logger.error(f"Unexpected error retrieving topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topics.")


# Get a Topic by ID
@router.get("/{topic_id}", response_model=TopicResponseWithContent)
def get_topic_and_its_content_by_id(topic_id: int, db: DBSessionDep):
    """
    Get a Topic and its Content by ID.

    Args:
        topic_id (int): The ID of the topic.

    Returns:
        TopicResponse: The topic with the specified ID.
    """
    logger.info("%s.get_topic_by_id: %s", __name__, topic_id)
    try:
        return topic_crud.read_topic_by_id(id=topic_id, db=db)
    except HTTPException as http_err:
        logger.error(f"Error retrieving topic: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error retrieving topic: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topic.")


# Get all topics and subtopics
@router.get("/{topic_id}/subtopics")
def get_topic_and_subtopics(topic_id: int, db: DBSessionDep):
    logger.info("%s.get_topic_and_subtopics: %s", __name__, topic_id)
    try:
        return topic_crud.read_topic_and_subtopics(id=topic_id, db=db)
    except HTTPException as http_err:
        logger.error(f"Error retrieving topics: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error retrieving topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topics.")


# Update a Topic by ID
@router.patch("/{topic_id}", response_model=TopicResponse)
def update_topic_by_id(topic_id: int, topic: TopicUpdate, db: DBSessionDep, course: CourseDep):
    """
    Update a topic by ID.

    Args:
        topic_id (int): The ID of the topic to update.
        topic (TopicUpdate): The updated topic data.

    Returns:
        TopicResponse: The updated topic.
    """
    logger.info("%s.update_topic_by_id: %s", __name__, topic_id)
    try:
        return topic_crud.update_topic(id=topic_id, topic=topic, db=db)
    except ValueError as e:
        logger.error(f"Error updating topic: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating topic: {e}")
        raise HTTPException(status_code=500, detail="Failed to update topic.")


# Delete a Topic by ID
@router.delete("/{topic_id}")
def delete_topic_by_id(topic_id: int, db: DBSessionDep):
    """
    Delete a topic by ID.

    Args:
        topic_id (int): The ID of the topic to delete.
    """
    logger.info("%s.delete_topic_by_id: %s", __name__, topic_id)
    try:
        return topic_crud.delete_topic(id=topic_id, db=db)
    except HTTPException as http_err:
        logger.error(f"Error deleting topic: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error deleting topic: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete topic.")

