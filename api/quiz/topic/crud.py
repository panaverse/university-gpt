from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select, text

from api.core.database import get_session
from api.quiz.topic.models import Topic, TopicBase, TopicCreate, TopicResponse, TopicUpdate

# Create a new topic [Recursive Topics]
def create_topic(topic: TopicCreate, db: Session = Depends(get_session)):
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
    topic_to_db = Topic.model_validate(topic)
    db.add(topic_to_db)
    db.commit()
    db.refresh(topic_to_db)
    return topic_to_db

# Get all topics
def read_topics(offset: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    """
    Retrieve a list of topics from the database.

    Args:
        offset (int): The number of topics to skip before starting to return results.
        limit (int): The maximum number of topics to return.
        db (optional) : Database Dependency Injection.

    Returns:
        List[Topic]: A list of Topic objects.

    """
    topics = db.exec(select(Topic).offset(offset).limit(limit)).all()
    return topics

# Get a Topic by Name
def get_topic_by_name(name: str, db: Session = Depends(get_session)):
    topic = db.exec(select(Topic).where(Topic.title == name)).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic

# Get a Topic by ID
def get_topic_by_id(id: int, db: Session = Depends(get_session)):
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
    topic = db.get(Topic, id)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic

# Update a Topic by ID
def update_topic(id: int, topic: TopicUpdate, db: Session = Depends(get_session)):
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
    topic_to_update = db.get(Topic, id)
    if not topic_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    topic_data = topic.model_dump(exclude_unset=True)
    for key, value in topic_data.items():
        setattr(topic_to_update, key, value)
    db.add(topic_to_update)
    db.commit()
    db.refresh(topic_to_update)
    return topic_to_update

# Delete a Topic by ID
def delete_topic(id: int, db: Session = Depends(get_session)):
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
    topic = db.get(Topic, id)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    db.delete(topic)
    db.commit()
    return {"message": "Topic deleted successfully"}