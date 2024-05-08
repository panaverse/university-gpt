from fastapi.testclient import TestClient
from sqlmodel import Session
import random
import pytest

from app import settings
from tests.utils.test_items import test_program_data
from app.crud.program_crud import program_crud


# fixture that gets all universities and returns the first one
@pytest.fixture
def program_id(db: Session):
    all_prgs = program_crud.get_all_programs_db(db=db, offset=0, per_page=10)
    return all_prgs[0].id


@pytest.fixture
def existing_course_id(client: TestClient, db: Session):
    # Get all courses first
    response = client.get(f"{settings.API_V1_STR}/course")
    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert response.json()["all_records"][0]["id"] is not None
    # Get by ID
    course_id = response.json()["all_records"][0]["id"]
    return course_id


def test_create_new_course(client: TestClient, program_id):
    updated_course_name = str(test_program_data.get("name")) + str(
        random.randint(1, 10000)
    )

    response = client.post(
        f"{settings.API_V1_STR}/course",
        json={"name": updated_course_name, "program_id": program_id},
    )
    assert response.status_code == 200
    assert response.json()["name"] == updated_course_name


def test_get_all_courses(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/course")
    assert response.status_code == 200
    assert response.json()["count"] >= 1

    assert response.json()["all_records"][0]["id"] is not None
    # Check previous
    assert response.json()["previous"] is None
    # all_records len
    assert len(response.json()["all_records"]) >= 1


def test_get_course_by_id(client: TestClient):
    # Get all courses first
    response = client.get(f"{settings.API_V1_STR}/course")
    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert response.json()["all_records"][0]["id"] is not None
    # Get by ID
    course_id = response.json()["all_records"][0]["id"]
    course_name = response.json()["all_records"][0]["name"]

    response = client.get(f"{settings.API_V1_STR}/course/{course_id}")
    assert response.status_code == 200
    assert response.json()["id"] == course_id
    assert response.json()["name"] == course_name


def test_update_course_by_id(client: TestClient, existing_course_id):
    updated_course_name = str(test_program_data.get("name")) + str(
        random.randint(1, 10000)
    )
    response = client.patch(
        f"{settings.API_V1_STR}/course/{existing_course_id}",
        json={"name": updated_course_name},
    )
    assert response.status_code == 200
    assert response.json()["name"] == updated_course_name


def test_delete_course_by_id(client: TestClient, existing_course_id):
    response = client.delete(f"{settings.API_V1_STR}/course/{existing_course_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Course deleted"}


def test_get_course_invalid_id(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/course/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Course not found"}


def test_update_course_invalid_id(client: TestClient):
    response = client.patch(
        f"{settings.API_V1_STR}/course/100", json={"name": "Course of Temp Test"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Course not found"}


def test_delete_course_invalid_id(client: TestClient):
    response = client.delete(f"{settings.API_V1_STR}/course/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Course not found"}


def test_get_all_courses_invalid_page(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/course?page=-1")
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {
            "type": "greater_than_equal",
            "loc": ["query", "page"],
            "msg": "Input should be greater than or equal to 1",
            "input": "-1",
            "ctx": {"ge": 1},
        }
    ]


def test_get_all_courses_invalid_per_page(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/course?per_page=0")
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {
            "type": "greater_than_equal",
            "loc": ["query", "per_page"],
            "msg": "Input should be greater than or equal to 1",
            "input": "0",
            "ctx": {"ge": 1},
        }
    ]
