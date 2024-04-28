from fastapi.testclient import TestClient
from sqlmodel import Session
import random
import pytest

from app import settings
from app.init_data import program_name
from tests.utils.test_items import test_program_data
from app.crud.university_crud import university_crud

# fixture that get all universities and return the first one is
@pytest.fixture
def university_id(db: Session):
    all_universities = university_crud.get_all_universities_db(db=db, offset=0, per_page=10)
    return all_universities[0].id

@pytest.fixture
def existing_program_id(client: TestClient, db: Session):
        # Get all first
    response = client.get(f"{settings.API_V1_STR}/program")
    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert response.json()["all_records"][0]["id"] is not None
    # Get by ID
    prg_id = response.json()["all_records"][0]["id"]
    return prg_id

def test_create_new_program(
    client: TestClient,
    university_id
):
    updated_program_name = test_program_data.get("name") + str(random.randint(1, 10000))
    
    response = client.post(
        f"{settings.API_V1_STR}/program",
        json={
            "name": updated_program_name,
            "university_id": university_id
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == updated_program_name

def test_get_all_programs(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/program")
    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert response.json()["all_records"][0]["id"] is not None
    assert response.json()["all_records"][0]["name"] == program_name
    # Check previous
    assert response.json()["previous"] == None
    # all_records len
    assert len(response.json()["all_records"]) >= 1

def test_get_program_by_id(
    client: TestClient
):
    # Get all first
    response = client.get(f"{settings.API_V1_STR}/program")
    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert response.json()["all_records"][0]["id"] is not None
    # Get by ID
    prg_id = response.json()["all_records"][0]["id"]
    prg_name = response.json()["all_records"][0]["name"]

    response = client.get(f"{settings.API_V1_STR}/program/{prg_id}")
    assert response.status_code == 200
    assert response.json()["id"] == prg_id
    assert response.json()["name"] == prg_name

def test_update_program_by_id(
    client: TestClient,
    existing_program_id
):

    updated_program_name = test_program_data.get("name") + str(random.randint(1, 10000))
    response = client.patch(
        f"{settings.API_V1_STR}/program/{existing_program_id}",
        json={"name": updated_program_name}
    )
    assert response.status_code == 200
    assert response.json()["name"] == updated_program_name

def test_delete_program_by_id(
    client: TestClient,
    existing_program_id
):
    response = client.delete(f"{settings.API_V1_STR}/program/{existing_program_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Program deleted"}
   

def test_get_program_invalid_id(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/program/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Program not found"}

def test_update_program_invalid_id(
    client: TestClient
):
    response = client.patch(
        f"{settings.API_V1_STR}/program/100",
        json={"name": "Program of Temp Test"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Program not found"}

def test_delete_program_invalid_id(
    client: TestClient
):
    response = client.delete(f"{settings.API_V1_STR}/program/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Program not found"}

def test_get_all_programs_invalid_page(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/program?page=-1")
    assert response.status_code == 422
    assert response.json()["detail"] == [{'type': 'greater_than_equal', 
                                            'loc': ['query', 'page'], 
                                            'msg': 'Input should be greater than or equal to 1', 
                                            'input': '-1', 'ctx': {'ge': 1}
                                        }]

def test_get_all_programs_invalid_per_page(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/program?per_page=0")
    assert response.status_code == 422
    assert response.json()["detail"] == [{'type': 'greater_than_equal', 
                                          'loc': ['query', 'per_page'], 
                                          'msg': 'Input should be greater than or equal to 1', 
                                          'input': '0', 'ctx': {'ge': 1}
                                        }]
