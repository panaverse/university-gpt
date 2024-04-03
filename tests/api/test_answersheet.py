import datetime
import pytest
import random
import math
from httpx import AsyncClient
from typing import AsyncGenerator

from app.core import settings
from app.main import app
from app import init_data
from app.pre_start_tests import TestAsyncSessionLocal
from app.core.db import get_async_session
from app.models.answersheet_models import AnswerSlotCreate, AnswerSlotRead
from app.models.base import QuestionTypeEnum


async def override_session():
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_async_session] = override_session
    async with AsyncClient(app=app, base_url=settings.DEV_URL) as client:
        yield client


# Fixture to Get New Quiz Key
@pytest.fixture(scope="function")
async def get_new_quiz_key(test_client):
    # Create an InActivate QuizKey
    start_time = datetime.datetime.now()
    time_limit_sec = 3  # Assuming 3 days for the time limit
    time_limit_interval = datetime.timedelta(milliseconds=time_limit_sec)
    end_time = start_time + datetime.timedelta(microseconds=time_limit_sec)
    time_limit_interval = time_limit_interval.total_seconds()

    async for client in test_client:
        key_inital = "Key"
        # Generate A Radom Number to add tp Key
        key_inital += str(math.floor(random.random() * 1000))
        key_response = await client.post(
            "/api/v1/quiz-engine/quiz-setting",
            json={
                "quiz_id": init_data.quiz.id or 1,
                "instructions": "Attempt Carefully",
                "time_limit": time_limit_interval,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "quiz_key": key_inital,
            },
        )
        assert key_response is not None

        Quiz_Key = key_response.json()["quiz_key"]
        return Quiz_Key


@pytest.mark.asyncio
async def test_generate_runtime_quiz_for_student(test_client, get_new_quiz_key):
    quiz_key = await get_new_quiz_key

    async for client in test_client:
        new_student = await client.post(
            "/api/v1/user/student",
            json={
                "student_id": math.floor(random.random() * 1000),
            },
        )
        new_student_id = new_student.json()["student_id"]
        # Await the coroutine to get the actual quiz key value

        response = await client.post(
            "/api/v1/answersheet/attempt",
            json={
                "student_id": new_student_id,
                "quiz_id": init_data.quiz.id or 1,
                "quiz_key": quiz_key,
            },
        )
        assert response is not None
        assert response.status_code == 200

        # Convert timedelta to string representation
        time_limit_str = init_data.quiz_setting.time_limit.days
        assert response.json() == {
            "answer_sheet_id": response.json()["answer_sheet_id"],
            "quiz_title": init_data.quiz.quiz_title,
            "course_id": init_data.quiz.course_id or 1,
            "instructions": init_data.quiz_setting.instructions,
            "student_id": new_student_id,
            "quiz_id": init_data.quiz.id or 1,
            "time_limit": f"P{time_limit_str}D",  # Convert to string representation
            "time_start": response.json()["time_start"],
            "total_points": init_data.quiz.total_points,
            "quiz_key": quiz_key,
            "quiz_questions": response.json()["quiz_questions"],
        }


@pytest.mark.asyncio
async def test_generate_runtime_quiz_for_student_with_invalid_quiz_key(test_client):
    async for client in test_client:
        response = await client.post(
            "/api/v1/answersheet/attempt",
            json={
                "student_id": init_data.student.student_id,
                "quiz_id": init_data.quiz.id or 1,
                "quiz_key": "InvalidKey",
            },
        )
    assert response is not None
    assert response.json() == {"detail": "QuizSetting not found"}
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_generate_runtime_quiz_for_student_with_invalid_quiz_id(
    test_client, get_new_quiz_key
):
    quiz_key = await get_new_quiz_key

    async for client in test_client:
        response = await client.post(
            "/api/v1/answersheet/attempt",
            json={
                "student_id": init_data.student.student_id,
                "quiz_id": 1000,
                "quiz_key": quiz_key,
            },
        )
        assert response is not None
        assert response.json() == {"detail": "QuizSetting not found"}
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_generate_runtime_quiz_for_student_with_ongoing_attempt(
    test_client, get_new_quiz_key
):
    quiz_key = await get_new_quiz_key

    async for client in test_client:
        # Simulate an ongoing attempt for the student
        response = await client.post(
            "/api/v1/answersheet/attempt",
            json={
                "student_id": math.floor(random.random() * 1000),
                "quiz_id": init_data.quiz.id or 1,
                "quiz_key": quiz_key,
            },
        )
        assert response is not None

        # Try to start another attempt for the same quiz for the same student
        response_2 = await client.post(
            "/api/v1/answersheet/attempt",
            json={
                "student_id": init_data.student.student_id,
                "quiz_id": init_data.quiz.id or 1,
                "quiz_key": quiz_key,
            },
        )
        assert response_2 is not None
        assert response_2.status_code == 400
        assert response_2.json() == {"detail": "You have an ongoing quiz attempt"}


@pytest.mark.asyncio
async def test_generate_runtime_quiz_for_student_with_finished_attempt(
    test_client, get_new_quiz_key
):
    quiz_key = await get_new_quiz_key

    async for client in test_client:
        # Simulate an ongoing attempt for the student
        response = await client.post(
            "/api/v1/answersheet/attempt",
            json={
                "student_id": math.floor(random.random() * 1000),
                "quiz_id": init_data.quiz.id or 1,
                "quiz_key": quiz_key,
            },
        )
        assert response is not None
        assert response.status_code == 200
        # Finish the Attempt
        response_2 = await client.patch(
            f"/api/v1/answersheet/{response.json()["answer_sheet_id"]}/finish",
        )
        assert response_2 is not None
        assert response_2.status_code == 200
        # Try to start another attempt for the same quiz for the same student
        response_2 = await client.post(
            "/api/v1/answersheet/attempt",
            json={
                "student_id": response.json()["student_id"],
                "quiz_id": init_data.quiz.id or 1,
                "quiz_key": quiz_key,
            },
        )
        assert response_2 is not None
        assert response_2.status_code == 400
        assert response_2.json() == {"detail": "You have already attempted this quiz"}


# PATCH Path: /api/v1/answersheet/{quiz_attempt_id}/finish


@pytest.mark.asyncio
async def test_finish_quiz_attempt(test_client, get_new_quiz_key):
    quiz_key = await get_new_quiz_key
    async for client in test_client:
        response = await client.post(
            "/api/v1/answersheet/attempt",
            json={
                "student_id": math.floor(random.random() * 1000),
                "quiz_id": init_data.quiz.id or 1,
                "quiz_key": quiz_key,
            },
        )
        assert response is not None
        assert response.json()["answer_sheet_id"] == response.json()["answer_sheet_id"]
        assert response.status_code == 200

        answer_sheet_id = response.json()["answer_sheet_id"]

        response_2 = await client.patch(
            f"/api/v1/answersheet/{answer_sheet_id}/finish",
        )
        assert response_2 is not None
        assert response_2.status_code == 200


@pytest.mark.asyncio
async def test_finish_quiz_attempt_with_invalid_id(test_client):
    async for client in test_client:
        response = await client.patch(
            "/api/v1/answersheet/100000/finish",
        )
        assert response is not None
        assert response.status_code == 404
        assert response.json() == {"detail": "Invalid Quiz Attempt ID"}


# GET Path: /api/v1/answersheet/{quiz_attempt_id}
@pytest.mark.asyncio
async def test_get_quiz_attempt_by_id_invalid_id(test_client):
    async for client in test_client:
        response = await client.get("/api/v1/answersheet/100000?student_id=1")
        assert response is not None
        assert response.status_code == 404
        assert response.json() == {"detail": "Quiz Attempt Not Found"}


@pytest.mark.asyncio
async def test_get_quiz_attempt_by_id_no_student_id(test_client):
    async for client in test_client:
        response = await client.get(
            "/api/v1/answersheet/1000",
        )
        assert response is not None
        assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.asyncio
async def test_get_quiz_attempt_by_id_str_quiz_attempt_id(test_client):
    async for client in test_client:
        response = await client.get("/api/v1/answersheet/abcd?student_id=1")
        assert response.status_code == 422  # Not Found


# POST: QuizAnswerSlot - /api/v1/answersheet/answer_slot/save
@pytest.mark.asyncio
async def test_save_quiz_answer_slot_valid_attempt_id(test_client, get_new_quiz_key):
    quiz_key = await get_new_quiz_key
    # Create a New Quiz Attempt

    stu_id = math.floor(random.random() * 1000)
    async for client in test_client:
        attempt = await client.post(
            "/api/v1/answersheet/attempt",
            json={
                "student_id": stu_id,
                "quiz_id": init_data.quiz.id or 1,
                "quiz_key": quiz_key,
            },
        )
        assert attempt is not None
        assert attempt.status_code == 200

        # Create a valid AnswerSlotCreate object
        quiz_answer_slot = AnswerSlotCreate(
            quiz_answer_sheet_id=attempt.json()["answer_sheet_id"],
            question_id=attempt.json()["quiz_questions"][0]["id"],
            question_type=QuestionTypeEnum.single_select_mcq,
            selected_options_ids=[
                attempt.json()["quiz_questions"][0]["options"][0]["id"]
            ],
        )

    # Make a request to the endpoint
    async for client in test_client:
        response = await client.post(
            "/api/v1/answersheet/answer_slot/save",
            json={
                "student_id": stu_id,
                "quiz_answer_slot": quiz_answer_slot.model_dump_json(
                    exclude_unset=True
                ),
            },
        )

        # Assert the response status code is 200
        assert response.status_code == 200

        # Assert the response body matches the expected AnswerSlotRead model
        assert response.json() == AnswerSlotRead(
            id=response.json()["id"],
            quiz_answer_sheet_id=attempt.json()["answer_sheet_id"],
            question_id=attempt.json()["quiz_questions"][0]["id"],
            question_type=QuestionTypeEnum.single_select_mcq,
        ).model_dump_json(exclude_unset=True)


@pytest.mark.asyncio
async def test_save_quiz_answer_slot_invalid_attempt_id(test_client):
    # Create an invalid AnswerSlotCreate object with an invalid quiz_answer_sheet_id
    student_id = math.floor(random.random() * 1000)
    answer_sheet_id = math.floor(random.random() * 1000)

    # Make a request to the endpoint
    async for client in test_client:
        response = await client.post(
            f"/api/v1/answersheet/answer_slot/save?student_id={student_id}",
            json={
                "quiz_answer_sheet_id": answer_sheet_id,
                "question_id": 7,
                "question_type": QuestionTypeEnum.single_select_mcq,
                "selected_options_ids": [1],
            },
        )

        # Assert the response body matches the expected error message
        assert response.json() == {"detail": "Invalid Quiz Attempt ID"}
        # Assert the response status code is 404
        assert response.status_code == 404


# Test when the quiz is not active
@pytest.mark.asyncio
async def test_save_quiz_answer_slot_quiz_not_active(test_client):
    # Create an InActivate QuizKey
    start_time = datetime.datetime.now()
    time_limit_sec = 3  # Assuming 3 days for the time limit
    time_limit_interval = datetime.timedelta(milliseconds=time_limit_sec)
    end_time = start_time + datetime.timedelta(microseconds=time_limit_sec)
    time_limit_interval = time_limit_interval.total_seconds()

    async for client in test_client:
        response = await client.post(
            "/api/v1/quiz-engine/quiz-setting",
            json={
                "quiz_id": init_data.quiz.id or 1,
                "instructions": "Attempt Carefully",
                "time_limit": time_limit_interval,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "quiz_key": "EXP",
            },
        )
        assert response is not None

        exp_quiz_key = response.json()["quiz_key"]

    # Create a New Quiz Attempt with a quiz that is not active
    stu_id = math.floor(random.random() * 1000)
    async for client in test_client:
        attempt = await client.post(
            "/api/v1/answersheet/attempt",
            json={
                "student_id": stu_id,
                "quiz_id": init_data.quiz.id or 1,
                "quiz_key": exp_quiz_key,
            },
        )
        assert attempt is not None
        assert attempt.status_code == 200

        # Create a valid AnswerSlotCreate object
        quiz_answer_slot = AnswerSlotCreate(
            quiz_answer_sheet_id=attempt.json()["answer_sheet_id"],
            question_id=attempt.json()["quiz_questions"][0]["id"],
            question_type=QuestionTypeEnum.single_select_mcq,
            selected_options_ids=[
                attempt.json()["quiz_questions"][0]["options"][0]["id"]
            ],
        )

        # Make a request to the endpoint
        response = await client.post(
            "/api/v1/answersheet/answer_slot/save",
            json={
                "student_id": stu_id,
                "quiz_answer_slot": quiz_answer_slot.model_dump_json(
                    exclude_unset=True
                ),
            },
        )

        # Assert the response status code is 404
        assert response.status_code == 404
        # Assert the response body matches the expected error message
        assert response.json() == {
            "detail": "Quiz Time has Ended or Invalid Quiz Attempt ID"
        }


# Test when the quiz attempt ID is invalid
@pytest.mark.asyncio
async def test_save_quiz_answer_slot_invalid_quiz_attempt_id(test_client):
    # Create a New Quiz Attempt with an invalid quiz attempt ID
    stu_id = math.floor(random.random() * 1000)
    async for client in test_client:
        # Make a request to the endpoint
        response = await client.post(
            f"/api/v1/answersheet/answer_slot/save?student_id={stu_id}",
            json={
                "quiz_answer_sheet_id": math.floor(random.random() * 1000),
                "question_id": 1,
                "question_type": QuestionTypeEnum.single_select_mcq,
                "selected_options_ids": [1],
            },
        )

        # Assert the response status code is 404
        assert response.status_code == 404
        # Assert the response body matches the expected error message
        assert response.json() == {"detail": "Invalid Quiz Attempt ID"}


@pytest.mark.asyncio
async def test_get_quiz_attempt_by_id_invalid_student_id(test_client):
    async for client in test_client:
        response = await client.get("/api/v1/answersheet/1?student_id=1000")
        assert response is not None
        assert response.status_code == 404
        assert response.json() == {"detail": "Quiz Attempt Not Found"}
