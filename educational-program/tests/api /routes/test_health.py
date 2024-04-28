from fastapi.testclient import TestClient
from app import settings

def test_container(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/container")
    assert response.status_code == 200
    assert response.json() == {"Container 1": "Educational Program!!!", "Port": "8000"}


def test_health(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/health")
    assert response.status_code == 200
    assert response.json() == {"app_status": "OK", "db_status": "OK", "environment": "development"}

def test_health_stats(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/health/stats")
    assert response.status_code == 200
    assert response.json()["university"] >= 0
    assert response.json()["program"] >= 0
    assert response.json()["course"] >= 0