from fastapi import HTTPException
from sqlmodel import Session
import random
import pytest
from tests.utils.test_items import temp_topic  # Ensure this is available in your test utils
from app.crud.topic_crud import topic_crud
from app.models.topic_models import TopicCreate, TopicUpdate
from app.init_data import init_topic_name, init_course_id
# Example fixture for creating a new topic
@pytest.fixture
def topic_id(db: Session):
    topic_name = temp_topic.get("title") + str(random.randint(1, 10000))
    topic = TopicCreate(title=topic_name, description="Test description", course_id= init_course_id)
    created_topic = topic_crud.create_topic(topic=topic, db=db)
    return created_topic.id

def test_create_topic(db: Session):
    topic_name = temp_topic.get("title") + str(random.randint(1, 10000))
    topic = TopicCreate(title=topic_name, description="Test description", course_id= init_course_id)
    created_topic = topic_crud.create_topic(topic=topic, db=db)
    
    assert created_topic.title == topic_name
    assert created_topic.description is not None
    assert created_topic.id is not None

def test_get_all_topics(db: Session):
    all_topics = topic_crud.read_topics(db=db, offset=0, per_page=10)
    assert all_topics is not None
    assert len(all_topics) > 0

def test_get_topic_by_id_valid(db: Session, topic_id):
    topic = topic_crud.read_topic_by_id(id=topic_id, db=db)
    assert topic is not None
    assert topic.id == topic_id

def test_update_topic_by_id(db: Session, topic_id):
    topic_name = temp_topic.get("title") + str(random.randint(1, 10000))
    topic = TopicUpdate(title=topic_name, course_id=init_course_id)
    updated_topic = topic_crud.update_topic(id=topic_id, topic=topic, db=db)
    
    assert updated_topic is not None
    assert updated_topic.id == topic_id
    assert updated_topic.title == topic_name

def test_delete_topic_by_id(db: Session, topic_id):
    result = topic_crud.delete_topic(id=topic_id, db=db)
    assert result == {"message": "Topic deleted successfully"}
    
    # Check if the topic is actually deleted
    with pytest.raises(HTTPException) as e:
        topic_crud.read_topic_by_id(id=topic_id, db=db)

# Test offset in get_all_topics
def test_get_all_topics_offset(db: Session):
    with pytest.raises(HTTPException) as e:
        topic_crud.read_topics(db=db, offset=1, per_page=0)
        assert e.value.status_code == 400
        assert e.value.detail == "Per page items cannot be less than 1"

# Get topic with invalid id
def test_get_topic_by_id_invalid(db: Session):
    with pytest.raises(HTTPException) as e:
        topic_crud.read_topic_by_id(id=100, db=db)
        assert e.value.status_code == 404
        assert e.value.detail == "Topic not found"


# Delete topic with invalid id
def test_delete_topic_invalid_id(db: Session):
    with pytest.raises(HTTPException) as e:
        topic_crud.delete_topic(id=10000, db=db)
        assert e.value.status_code == 404
        assert e.value.detail == "Topic not found"
