import pytest
import requests
from fastapi.testclient import TestClient
from tests.utils.test_items import temp_quiz_data, temp_topic, mock_course  # Ensure this is available in your test utils
from app import settings
# Fixture to get course_id
@pytest.fixture
def course_id():
    # Assuming you have a method to create or fetch a valid course ID
    return mock_course["id"]  # Example fixed ID for simplicity in testing

@pytest.fixture(autouse=True)
def existing_topic_id(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/topic")
    return response.json()["results"][0]["id"]
@pytest.fixture
def new_quiz_id(client: TestClient, existing_topic_id, course_id):
    quiz_data = temp_quiz_data.copy()
    quiz_data["add_topic_ids"] = [existing_topic_id]
    quiz_data["course_id"] = course_id

    response = client.post(
        f"{settings.API_V1_STR}/quiz",
        json=quiz_data
    )
    assert response.status_code == 200
    assert response.json()["quiz_title"] == quiz_data["quiz_title"]
    return response.json()["id"]

def test_create_new_quiz(client: TestClient, existing_topic_id, course_id):
    quiz_data = temp_quiz_data.copy()
    quiz_data["add_topic_ids"] = [existing_topic_id]
    quiz_data["course_id"] = course_id

    response = client.post(
        f"{settings.API_V1_STR}/quiz",
        json=quiz_data
    )
    assert response.status_code == 200
    assert response.json()["quiz_title"] == quiz_data["quiz_title"]

def test_read_all_quizzes(client: TestClient, course_id):
    response = client.get(f"{settings.API_V1_STR}/quiz/all/{course_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_quiz_by_id(client: TestClient, new_quiz_id):
    response = client.get(f"{settings.API_V1_STR}/quiz/{new_quiz_id}")
    assert response.status_code == 200
    assert response.json()["id"] == new_quiz_id

def test_update_existing_quiz(client: TestClient, new_quiz_id):
    updated_quiz_data = {"quiz_title": "Updated Quiz Name"}
    response = client.patch(
        f"{settings.API_V1_STR}/quiz/{new_quiz_id}",
        json=updated_quiz_data
    )
    assert response.status_code == 200
    assert response.json()["quiz_title"] == updated_quiz_data["quiz_title"]

def test_delete_existing_quiz(client: TestClient, new_quiz_id):
    response = client.delete(f"{settings.API_V1_STR}/quiz/delete/{new_quiz_id}")
    assert response.status_code == 200
    assert response.json() == {'message': 'Quiz deleted successfully!'}
    
    
def test_quiz_not_found(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/quiz/9999")  # Assume 9999 is a non-existing ID
    assert response.status_code == 400
    assert response.json()["detail"] == "Error in fetching Quiz"


def test_create_new_quiz_invalid_data(client: TestClient):
    invalid_quiz_data = {"name": ""}  # Assuming 'name' cannot be empty
    response = client.post(
        f"{settings.API_V1_STR}/quiz",
        json=invalid_quiz_data
    )
    assert response.status_code == 422
    assert "detail" in response.json()
