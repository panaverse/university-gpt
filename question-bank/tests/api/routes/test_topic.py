from fastapi.testclient import TestClient
from sqlmodel import Session
import random
import pytest
from app.init_data import init_topic_name, init_sub_topic_name
from app import settings
from tests.utils.test_items import temp_topic

@pytest.fixture
def existing_topic_id(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/topic")
    return response.json()["results"][0]["id"]

@pytest.fixture
def new_topic_id(client: TestClient):
    response = client.post(
    f"{settings.API_V1_STR}/topic",
    json=temp_topic
    )
    return response.json()["id"]

def test_create_new_topic(
    client: TestClient,
):
    response = client.post(
    f"{settings.API_V1_STR}/topic",
    json=temp_topic
    )
    assert response.status_code == 200
    assert response.json()["title"] == temp_topic["title"]

def test_get_all_topics(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/topic")
    assert response.status_code == 200
    assert response.json()["count"] >= 1

    assert response.json()["results"][0]["id"] is not None
    # Check previous
    assert response.json()["previous"] == None
    # results len
    assert len(response.json()["results"]) >= 1

def test_get_topic_by_id(
    client: TestClient
):
    # Get all topics first
    response = client.get(f"{settings.API_V1_STR}/topic")
    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert response.json()["results"][0]["id"] is not None
    # Get by ID
    topic_id = response.json()["results"][0]["id"]
    topic_name = response.json()["results"][0]["title"]

    response = client.get(f"{settings.API_V1_STR}/topic/{topic_id}")
    assert response.status_code == 200
    assert response.json()["id"] == topic_id
    assert response.json()["title"] == topic_name

def test_update_topic_by_id(
    client: TestClient,
    existing_topic_id
):

    updated_topic_name = "named_topic" + str(random.randint(1, 10000))
    response = client.patch(
        f"{settings.API_V1_STR}/topic/{existing_topic_id}",
        json={"title": updated_topic_name, "course_id": 1}
    )
    assert response.status_code == 200
    assert response.json()["title"] == updated_topic_name

def test_delete_topic_by_id(
    client: TestClient,
    new_topic_id
):
    response = client.delete(f"{settings.API_V1_STR}/topic/{new_topic_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Topic deleted successfully"}

def test_get_topic_invalid_id(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/topic/10000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Topic not found"}

def test_update_topic_missing_course_id(
    client: TestClient
):
    response = client.patch(
        f"{settings.API_V1_STR}/topic/1000",
        json={"name": "Topic of Temp Test"}
    )
    assert response.status_code == 422

def test_update_topic_invalid_id(
    client: TestClient
):
    response = client.patch(
        f"{settings.API_V1_STR}/topic/1000",
        json={"name": "Topic of Temp Test", "course_id": 1}
    )
    assert response.status_code == 404

def test_delete_topic_invalid_id(
    client: TestClient
):
    response = client.delete(f"{settings.API_V1_STR}/topic/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Topic not found"}

def test_get_all_topics_invalid_page(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/topic?page=-1")
    assert response.status_code == 422
    assert response.json()["detail"] == [{'type': 'greater_than_equal', 
                                            'loc': ['query', 'page'], 
                                            'msg': 'Input should be greater than or equal to 1', 
                                            'input': '-1', 'ctx': {'ge': 1}
                                        }]

def test_get_all_topics_invalid_per_page(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/topic?per_page=0")
    assert response.status_code == 422
    assert response.json()["detail"] == [{'type': 'greater_than_equal', 
                                          'loc': ['query', 'per_page'], 
                                          'msg': 'Input should be greater than or equal to 1', 
                                          'input': '0', 'ctx': {'ge': 1}
                                        }]
# 1. Test creating a new topic with invalid course ID
def test_create_new_topic_invalid_course_id(client: TestClient):
    temp_topic_with_invalid_course = temp_topic.copy()
    temp_topic_with_invalid_course["course_id"] = 9999  # Assuming 9999 is an invalid ID
    response = client.post(
        f"{settings.API_V1_STR}/topic",
        json=temp_topic_with_invalid_course
    )
    assert response.status_code == 404
    assert 'Course not found' in response.json()["detail"]

# 2. Test retrieving a topic and its subtopics with a valid ID
def test_get_topic_and_subtopics_valid_id(client: TestClient, existing_topic_id):
    response = client.get(f"{settings.API_V1_STR}/topic/{existing_topic_id}/subtopics")
    assert response.status_code == 200
    assert "children_topics" in response.json()

# 3. Test retrieving a topic and its subtopics with an invalid ID
def test_get_topic_and_subtopics_invalid_id(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/topic/9999/subtopics")  # Assuming 9999 is an invalid ID
    assert response.status_code == 404
    assert "Topic not found" in response.json()["detail"]

# 4. Test updating a topic with a non-existing course
def test_update_topic_non_existing_course(client: TestClient, existing_topic_id):
    updated_topic_data = {"title": "Updated Topic", "course_id": 9999}  # Assuming 9999 is an invalid course ID
    response = client.patch(
        f"{settings.API_V1_STR}/topic/{existing_topic_id}",
        json=updated_topic_data
    )
    assert response.status_code == 404
    assert 'Course not found' in response.json()["detail"]

# 5. Test deleting a topic with a valid ID
def test_delete_existing_topic(client: TestClient, new_topic_id):
    # Make sure the topic is present before deletion
    get_response = client.get(f"{settings.API_V1_STR}/topic/{new_topic_id}")
    assert get_response.status_code == 200

    # Now delete the topic
    del_response = client.delete(f"{settings.API_V1_STR}/topic/{new_topic_id}")
    assert del_response.status_code == 200
    assert "Topic deleted successfully" in del_response.json()["message"]

# 6. Test creating a topic with missing required fields
def test_create_topic_missing_fields(client: TestClient):
    incomplete_topic = {"description": "A topic without a title or course_id."}
    response = client.post(
        f"{settings.API_V1_STR}/topic",
        json=incomplete_topic
    )
    assert response.status_code == 422
    assert "title" in response.json()["detail"][0]["loc"]

# 7. Test getting all topics with a high per_page value
def test_get_all_topics_high_per_page(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/topic?per_page=100")
    assert response.status_code == 200
    assert len(response.json()["results"]) <= 100


# 8. Test updating a topic with missing fields (partial update)
def test_partial_update_topic(client: TestClient, existing_topic_id):
    partial_update = {"title": "Partially Updated Title", "course_id": 1}
    response = client.patch(
        f"{settings.API_V1_STR}/topic/{existing_topic_id}",
        json=partial_update
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Partially Updated Title"

# 9. Test updating a topic by ID with invalid data types (e.g., string for an integer field)
def test_update_topic_invalid_data_types(client: TestClient, existing_topic_id):
    invalid_data = {"course_id": "not_an_integer"}
    response = client.patch(
        f"{settings.API_V1_STR}/topic/{existing_topic_id}",
        json=invalid_data
    )
    assert response.status_code == 422