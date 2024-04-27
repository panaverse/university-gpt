from fastapi.testclient import TestClient
import pytest
import random
from app import settings
from tests.utils.test_items import temp_question  # Ensure this is available in your test utils

@pytest.fixture
def new_question_id(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/question",
        json=temp_question
    )
    return response.json()["id"]

def test_create_new_question(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/question",
        json=temp_question
    )
    assert response.json()["question_text"] == temp_question["question_text"]
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