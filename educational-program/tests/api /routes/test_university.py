from fastapi.testclient import TestClient
from app import settings

from app.init_data import university_name
from tests.utils.test_items import test_uni_data

def test_get_single_university(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/university/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == university_name

def test_get_all_universities(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/university")
    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert response.json()["all_records"][0]["id"] is not None
    assert response.json()["all_records"][0]["name"] == university_name
    # Check previous
    assert response.json()["previous"] == None
    # all_records len
    assert len(response.json()["all_records"]) >= 1

def test_create_university(
    client: TestClient
):
    test_uni_data = {
        "name": "University of Temp Test",
        "description": "This is a temporary test university"
    }
    response = client.post(
        f"{settings.API_V1_STR}/university",
        json=test_uni_data
    )
    assert response.status_code == 200
    assert response.json()["name"] == test_uni_data.get("name")
    assert response.json()["description"] == test_uni_data.get("description")

def test_update_university(
    client: TestClient
):
    temp_uni_name = "University of Temp Test"
    response = client.patch(
        f"{settings.API_V1_STR}/university/1",
        json={"name": temp_uni_name}
    )
    assert response.status_code == 200
    assert response.json()["name"] == temp_uni_name

def test_delete_university(
    client: TestClient
):
    response = client.delete(f"{settings.API_V1_STR}/university/1")
    assert response.status_code == 200
    assert response.json() == {"message": "University deleted"}
    # Check if the university is deleted
    response = client.get(f"{settings.API_V1_STR}/university/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "University not found"}

def test_create_university_duplicate(
    client: TestClient
):
    # Create Uni
    response = client.post(
        f"{settings.API_V1_STR}/university",
        json=test_uni_data
    )

    response = client.post(
        f"{settings.API_V1_STR}/university",
        json=test_uni_data
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "University with same name already exists"}
   
# get uni with invalid id 
def test_get_university_invalid_id(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/university/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "University not found"}

# update uni with invalid id
def test_update_university_invalid_id(
    client: TestClient
):
    response = client.patch(
        f"{settings.API_V1_STR}/university/100",
        json={"name": "University of Temp Test"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "university not found"}

# delete uni with invalid id
def test_delete_university_invalid_id(
    client: TestClient
):
    response = client.delete(f"{settings.API_V1_STR}/university/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "University not found"}

# get all unis with invalid page
def test_get_all_universities_invalid_page(
    client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/university?page=-1")
    assert response.status_code == 422
    assert response.json()["detail"] == [{'type': 'greater_than_equal', 
                                            'loc': ['query', 'page'], 
                                            'msg': 'Input should be greater than or equal to 1', 
                                            'input': '-1', 'ctx': {'ge': 1}
                                        }]

def test_get_all_universities_invalid_per_page(
        client: TestClient
):
    response = client.get(f"{settings.API_V1_STR}/university?per_page=0")
    assert response.status_code == 422
    assert response.json()["detail"] == [{'type': 'greater_than_equal', 
                                          'loc': ['query', 'per_page'], 
                                          'msg': 'Input should be greater than or equal to 1', 
                                          'input': '0', 'ctx': {'ge': 1}
                                          }]