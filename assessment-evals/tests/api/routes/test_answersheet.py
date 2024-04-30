from fastapi.testclient import TestClient
import pytest
from app import settings

# Handle testing edge cases, such as invalid inputs or unauthorized access
def test_generate_runtime_quiz_invalid_key(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/attempt",
        json={"quiz_id": 1, "quiz_key": "invalid-key"},
        headers={"Authorization": "Bearer valid-token"}
    )
    assert response.status_code == 404
    assert "detail" in response.json()
    
# # Test for generating a runtime quiz for a student
# def test_generate_runtime_quiz_for_student(client: TestClient):
#     response = client.post(
#         f"{settings.API_V1_STR}/attempt",
#         json={"quiz_id": 1, "quiz_key": "valid-key"},
#         headers={"Authorization": "Bearer valid-token"}
#     )
#     assert response.status_code == 200
#     assert "quiz_questions" in response.json()

# # Test for getting a quiz attempt by ID
# def test_get_quiz_attempt_by_id(client: TestClient):
#     response = client.get(
#         f"{settings.API_V1_STR}/123",  # Assuming 123 is a valid quiz attempt ID
#         headers={"Authorization": "Bearer valid-token"}
#     )
#     assert response.status_code == 200
#     assert response.json()["id"] == 123

# # Test for updating a quiz attempt to finish it
# def test_update_quiz_attempt(client: TestClient):
#     response = client.patch(
#         f"{settings.API_V1_STR}/123/finish",  # Assuming 123 is a valid answer sheet ID
#         headers={"Authorization": "Bearer valid-token"}
#     )
#     assert response.status_code == 200
#     assert "finished_at" in response.json()

# # Test for saving a quiz answer slot
# def test_save_quiz_answer_slot(client: TestClient):
#     response = client.post(
#         f"{settings.API_V1_STR}/answer_slot/save",
#         json={"answer_slot_data": "example data"},
#         headers={"Authorization": "Bearer valid-token"}
#     )
#     assert response.status_code == 200
#     assert "answer_slot_id" in response.json()

# # Test for retrieving all answers for a given quiz attempt
# def test_get_quiz_feedback(client: TestClient):
#     response = client.get(
#         f"{settings.API_V1_STR}/123/view-all-answers",  # Assuming 123 is a valid answer sheet ID
#         headers={"Authorization": "Bearer valid-token"}
#     )
#     assert response.status_code == 200
#     assert "overview" in response.json()
#     assert "quiz_answers_attempted" in response.json()["overview"]

# def test_unauthorized_access(client: TestClient):
#     response = client.get(
#         f"{settings.API_V1_STR}/123",  # Assuming 123 is a valid quiz attempt ID
#         headers={"Authorization": "Bearer invalid-token"}
#     )
#     assert response.status_code == 401
#     assert "detail" in response.json()
