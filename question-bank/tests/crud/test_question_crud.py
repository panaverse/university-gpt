import random
import pytest
from fastapi import HTTPException
from sqlmodel import Session
from app.models.question_models import QuestionBankCreate, QuestionBankUpdate
from app.crud.question_crud import question_crud
from tests.utils.test_items import temp_question # this is available in your test utils
from app.init_data import init_course_id, init_topic_id  #  course ID is needed for questions

# Fixture to create a question
@pytest.fixture
def question_id(db: Session):
    question_data = QuestionBankCreate(
        question_text=temp_question.get("question_text") + str(random.randint(1, 10000)),
        question_type=temp_question.get("question_type"),
        topic_id=init_topic_id,
        difficulty=temp_question.get("difficulty"),
        is_verified= True,
        options=temp_question.get("options"),
    )
    created_question = question_crud.add_question(question=question_data, db=db)
    return created_question.id

def test_add_question(db: Session):
    question_text = temp_question.get("question_text") + str(random.randint(1, 10000))
    question_data = QuestionBankCreate(
        question_text=question_text,
        question_type=temp_question.get("question_type"),
        topic_id=init_topic_id,
        difficulty=temp_question.get("difficulty"),
        is_verified= True,
        options=temp_question.get("options"),
    )
    created_question = question_crud.add_question(question=question_data, db=db)
    assert created_question.question_text == question_text
    assert created_question.id is not None


def test_read_questions(db: Session):
    # TODO: Add Pagination to API ROUTE and update this test
    questions = question_crud.read_questions(db=db, offset=0, limit=10)
    assert isinstance(questions, list)
    assert len(questions) > 0

def test_get_question_by_id_valid(db: Session, question_id):
    question = question_crud.get_question_by_id(id=question_id, db=db)
    assert question is not None
    assert question.id == question_id

def test_update_question(db: Session, question_id):
    new_text = temp_question.get("question_text") + str(random.randint(1, 10000))
    question_update = QuestionBankUpdate(question_text=new_text)
    updated_question = question_crud.update_question(id=question_id, question=question_update, db=db)
    assert updated_question.question_text == new_text
    assert updated_question.id == question_id


def test_delete_question(db: Session, question_id):
    result = question_crud.delete_question(id=question_id, db=db)
    assert result == {"message": "Question deleted successfully"}
    
    # Verify deletion
    with pytest.raises(HTTPException) as e:
        question_crud.get_question_by_id(id=question_id, db=db)

def test_read_questions_by_type(db: Session):
    questions = question_crud.read_questions_by_type(question_type=temp_question.get("question_type"), db=db)
    assert isinstance(questions, list)
    assert len(questions) > 0  # Adjust based on expected outcomes

def test_get_questions_by_topic(db: Session):
    questions = question_crud.get_questions_by_topic(topic_id=init_topic_id, db=db)
    assert isinstance(questions, list)
    assert len(questions) >= 0  # Adjust based on expected outcomes
