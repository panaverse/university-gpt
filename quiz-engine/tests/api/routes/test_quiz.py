# import pytest
# from fastapi.testclient import TestClient
# from tests.utils.test_items import temp_quiz_data  # Ensure this is available in your test utils

# @pytest.fixture
# def new_quiz_id(client: TestClient):
#     response = client.post(
#         "/quizzes",  # Adjust the URL based on your actual API path
#         json=temp_quiz_data
#     )
#     return response.json()["id"]

# def test_create_new_quiz(client: TestClient):
#     quiz_data = temp_quiz_data.copy()
#     response = client.post(
#         "/quizzes",
#         json=quiz_data
#     )
#     assert response.status_code == 200
#     assert response.json()["name"] == quiz_data["name"]

# def test_read_all_quizzes(client: TestClient, course_id):
#     response = client.get(f"/quizzes/all/{course_id}")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_read_quiz_by_id(client: TestClient, new_quiz_id):
#     response = client.get(f"/quizzes/{new_quiz_id}")
#     assert response.status_code == 200
#     assert response.json()["id"] == new_quiz_id

# def test_update_existing_quiz(client: TestClient, new_quiz_id):
#     updated_quiz_data = {"name": "Updated Quiz Name"}
#     response = client.patch(
#         f"/quizzes/{new_quiz_id}",
#         json=updated_quiz_data
#     )
#     assert response.status_code == 200
#     assert response.json()["name"] == updated_quiz_data["name"]

# def test_delete_existing_quiz(client: TestClient, new_quiz_id):
#     response = client.delete(f"/quizzes/delete/{new_quiz_id}")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Quiz deleted successfully"}

# def test_quiz_not_found(client: TestClient):
#     response = client.get("/quizzes/9999")  # Assume 9999 is a non-existing ID
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Quiz not found"

# @pytest.fixture
# def course_id():
#     # Assuming you have a method to create or fetch a valid course ID
#     # This is a placeholder to represent fetching or creating a course
#     return 1  # Example fixed ID for simplicity in testing

# def test_create_new_quiz_invalid_data(client: TestClient):
#     invalid_quiz_data = {"name": ""}  # Assuming 'name' cannot be empty
#     response = client.post(
#         "/quizzes",
#         json=invalid_quiz_data
#     )
#     assert response.status_code == 422
#     assert "detail" in response.json()
