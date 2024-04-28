from fastapi.testclient import TestClient
from sqlmodel import Session
import random
import pytest
from app import settings
from tests.utils.test_items import temp_topic  # Ensure this is available in your test utils
from tests.utils.test_items import temp_question  # Ensure this is available in your test utils
from app.init_data import init_course_id
from app.crud.topic_crud import topic_crud
from app.models.topic_models import TopicCreate

# Example fixture for creating a new topic
@pytest.fixture
def topic_id(db: Session):
    topic_name = temp_topic.get("title") + str(random.randint(1, 10000))
    topic = TopicCreate(title=topic_name, description="Test description", course_id= init_course_id)
    created_topic = topic_crud.create_topic(topic=topic, db=db)
    return created_topic.id

@pytest.fixture
def new_question_id(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/question",
        json=temp_question
    )
    return response.json()["id"]

def test_create_new_question(client: TestClient, topic_id):
    new_json_data = temp_question.copy()
    new_json_data["topic_id"] = topic_id
    response = client.post(
        f"{settings.API_V1_STR}/question",
        json=new_json_data
    )
    assert response.json()["question_text"] == new_json_data["question_text"]
    assert response.status_code == 200

def test_get_all_questions(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/question")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_question_by_id(client: TestClient, new_question_id):
    response = client.get(f"{settings.API_V1_STR}/question/{new_question_id}")
    assert response.status_code == 200
    assert response.json()["id"] == new_question_id

def test_update_question_by_id(client: TestClient, new_question_id):
    updated_text = "Updated question text" + str(random.randint(1, 10000))
    response = client.patch(
        f"{settings.API_V1_STR}/question/{new_question_id}",
        json={"question_text": updated_text}
    )
    assert response.status_code == 200
    assert response.json()["question_text"] == updated_text

def test_delete_question_by_id(client: TestClient, new_question_id):
    response = client.delete(f"{settings.API_V1_STR}/question/{new_question_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Question deleted successfully"}

def test_get_question_invalid_id(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/question/10000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}


def test_create_new_question_invalid_data(client: TestClient):
    incomplete_data = {"text": ""}
    response = client.post(
        f"{settings.API_V1_STR}/question",
        json=incomplete_data
    )
    assert response.status_code == 422
    assert (response.json()["detail"]) == [{'type': 'missing', 'loc': ['body', 'question_text'], 'msg': 'Field required', 'input': {'text': ''}}, {'type': 'missing', 'loc': ['body', 'topic_id'], 'msg': 'Field required', 'input': {'text': ''}}]