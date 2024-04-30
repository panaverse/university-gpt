import pytest
import random
from fastapi import HTTPException
from sqlmodel import Session
from app.models.quiz_models import QuizCreate, QuizUpdate
from app.crud.quiz_crud import quiz_engine
from tests.utils.test_items import temp_quiz_data, temp_topic
from app import settings
from fastapi.testclient import TestClient

@pytest.fixture
def new_topic_id(client: TestClient):
    response = client.post(
    f"{settings.API_V1_STR}/topic",
    json=temp_topic
    )
    return response.json()["id"]

@pytest.fixture
def quiz_id(db: Session, new_topic_id):  # Assuming topic_ids fixture is defined
    quiz_data = QuizCreate(
        quiz_title="Quiz" + str(random.randint(1000, 9999)),
        course_id=temp_quiz_data['course_id'],  # Use real or mocked course ID
        add_topic_ids=[new_topic_id],
        difficulty_level=temp_quiz_data['difficulty_level']
    )
    created_quiz = quiz_engine.create_quiz(quiz=quiz_data, db=db)
    return created_quiz.id

def test_create_quiz(db: Session, new_topic_id):
    quiz_name = "Quiz" + str(random.randint(1000, 9999))
    quiz_data = QuizCreate(
        quiz_title=quiz_name,
        course_id=temp_quiz_data['course_id'],
        add_topic_ids=[new_topic_id],
        difficulty_level=temp_quiz_data['difficulty_level']
    )
    created_quiz = quiz_engine.create_quiz(quiz=quiz_data, db=db)
    assert created_quiz.quiz_title == quiz_name
    assert created_quiz.id is not None

def test_read_quiz_by_id(db: Session, quiz_id):
    quiz = quiz_engine.read_quiz_by_id(quiz_id=quiz_id, db=db)
    assert quiz is not None
    assert quiz.id == quiz_id

def test_update_quiz(db: Session, quiz_id, new_topic_id):
    new_name = "Updated Quiz" + str(random.randint(1000, 9999))
    quiz_update_data = QuizUpdate(quiz_title=new_name, add_topic_ids=[new_topic_id])  # Assume topic_ids has multiple IDs
    updated_quiz = quiz_engine.update_quiz(quiz_id=quiz_id, quiz_update_data=quiz_update_data, db=db)
    assert updated_quiz.quiz_title == new_name
    assert updated_quiz.id == quiz_id

def test_delete_quiz(db: Session, quiz_id):
    result = quiz_engine.delete_quiz(quiz_id=quiz_id, db=db)
    assert result == {"message": "Quiz deleted successfully!"}
    
    with pytest.raises(HTTPException) as e:
        quiz_engine.read_quiz_by_id(quiz_id=quiz_id, db=db)

def test_read_all_quizzes_for_course(db: Session):  
    course_id = 1  # Use real or mocked course ID
    quizzes = quiz_engine.read_all_quizzes_for_course(db=db, course_id=course_id, offset=0, limit=10)
    assert isinstance(quizzes, list)
    assert len(quizzes) > 0

def test_quiz_not_found_error(db: Session):
    with pytest.raises(HTTPException) as e:
        quiz_engine.read_quiz_by_id(quiz_id=99999, db=db)  # Assume 99999 is an invalid ID
