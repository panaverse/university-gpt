import pytest
from fastapi import HTTPException
from sqlmodel import Session
from datetime import datetime, timedelta
from app.models.quiz_setting import QuizSettingCreate, QuizSettingUpdate
from app.crud.quiz_setting_crud import quiz_setting_engine
from app.models.quiz_models import QuizCreate
from app.crud.quiz_crud import quiz_engine
from tests.utils.test_items import temp_quiz_data 
import random
from app import settings
from fastapi.testclient import TestClient

@pytest.fixture(autouse=True)
def existing_topic_id(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/topic")
    return response.json()["results"][0]["id"]

@pytest.fixture
def quiz_id(db: Session, existing_topic_id):  # Assuming topic_ids fixture is defined
    quiz_data = QuizCreate(
        quiz_title="Quiz" + str(random.randint(1000, 9999)),
        course_id=temp_quiz_data['course_id'],  # Use real or mocked course ID
        add_topic_ids=[existing_topic_id],
       difficulty_level=temp_quiz_data['difficulty_level']
    )
    created_quiz = quiz_engine.create_quiz(quiz=quiz_data, db=db)
    return created_quiz.id

@pytest.fixture
def quiz_setting_id(db: Session, quiz_id):  # Assuming quiz_id is available from another fixture
    quiz_setting_data = QuizSettingCreate(
        quiz_id=quiz_id,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=2),
        quiz_key="securekey123",
        instructions="Do not cheat!",
        time_limit=60
    )
    created_quiz_setting = quiz_setting_engine.create_quiz_setting(db=db, quiz_setting=quiz_setting_data)
    return created_quiz_setting.id

def test_create_quiz_setting(db: Session, quiz_id):
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    quiz_setting_data = QuizSettingCreate(
        quiz_id=quiz_id,
        start_time=start_time,
        end_time=end_time,
        quiz_key="testkey2024",
        instructions="Do not cheat!",
        time_limit=60
    )
    created_quiz_setting = quiz_setting_engine.create_quiz_setting(db=db, quiz_setting=quiz_setting_data)
    assert created_quiz_setting.quiz_id == quiz_id
    assert created_quiz_setting.start_time == start_time.replace(tzinfo=None)  # Assuming UTC
    assert created_quiz_setting.end_time == end_time.replace(tzinfo=None)
    assert created_quiz_setting.quiz_key == "testkey2024"

def test_get_all_quiz_settings_for_quiz(db: Session, quiz_id):
    quiz_settings = quiz_setting_engine.get_all_quiz_settings_for_quiz(db=db, quiz_id=quiz_id)
    assert isinstance(quiz_settings, list)
    assert len(quiz_settings) >= 0

def test_get_quiz_setting_by_id(db: Session, quiz_setting_id):
    quiz_setting = quiz_setting_engine.get_quiz_setting_by_id(db=db, quiz_setting_id=quiz_setting_id)
    assert quiz_setting is not None
    assert quiz_setting.id == quiz_setting_id

def test_update_quiz_setting(db: Session, quiz_setting_id):
    new_end_time = datetime.now() + timedelta(hours=3)
    quiz_setting_update = QuizSettingUpdate(end_time=new_end_time)
    updated_quiz_setting = quiz_setting_engine.update_quiz_setting(db=db, quiz_setting_id=quiz_setting_id, quiz_setting_update=quiz_setting_update)
    assert updated_quiz_setting.end_time == new_end_time.replace(tzinfo=None)

def test_remove_quiz_setting(db: Session, quiz_setting_id):
    result = quiz_setting_engine.remove_quiz_setting(db=db, quiz_setting_id=quiz_setting_id)
    assert result == {"message": "QuizSetting deleted successfully!"}
    
    with pytest.raises(HTTPException) as exc:
        quiz_setting_engine.get_quiz_setting_by_id(db=db, quiz_setting_id=quiz_setting_id)
        assert exc.value.status_code == 404

def test_validate_quiz_key(db: Session, quiz_setting_id):
    quiz_setting = quiz_setting_engine.get_quiz_setting_by_id(db=db, quiz_setting_id=quiz_setting_id)
    valid_key = quiz_setting.quiz_key
    validated_quiz_setting = quiz_setting_engine.validate_quiz_key(db=db, quiz_id=quiz_setting.quiz_id, quiz_key=valid_key)
    assert validated_quiz_setting == quiz_setting

def test_validate_quiz_key_invalid(db: Session, quiz_id):
    with pytest.raises(HTTPException) as exc:
        quiz_setting_engine.validate_quiz_key(db=db, quiz_id=quiz_id, quiz_key="invalidkey")
    assert exc.value.status_code == 404
    assert "QuizSetting not found" in exc.value.detail

