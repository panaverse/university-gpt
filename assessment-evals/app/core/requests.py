from fastapi import HTTPException
from requests import get
from app import settings
from app.core.utils import load_error_json

def get_course(course_id: int):
    course_request = get(f"{settings.EDUCATIONAL_PROGRAM_URL}/api/v1/course/{course_id}")
    if course_request.status_code == 200:
        return course_request.json()
    raise HTTPException(status_code=course_request.status_code, detail=load_error_json(course_request))

# get a question by id
def get_question(question_id: int):
    question_request = get(f"{settings.QUIZ_ENGINE_API_URL}/api/v1/question/{question_id}")
    if question_request.status_code == 200:
        return question_request.json()
    raise HTTPException(status_code=question_request.status_code, detail=load_error_json(question_request))

# Get Runtime Quiz Questions
def get_runtime_quiz_questions(quiz_id: int):
    quiz_request = get(f"{settings.QUIZ_ENGINE_API_URL}/api/v1/wrapper/runtime-generation?quiz_id={quiz_id}")
    if quiz_request.status_code == 200:
        return quiz_request.json()
    raise HTTPException(status_code=quiz_request.status_code, detail=load_error_json(quiz_request))

# Validate Quiz Key
def validate_quiz_key(quiz_id: int, quiz_key: str):
    quiz_key_request = get(f"{settings.QUIZ_ENGINE_API_URL}/api/v1/wrapper/validate-quiz-key?quiz_id={quiz_id}&quiz_key={quiz_key}")
    if quiz_key_request.status_code == 200:
        return quiz_key_request.json()
    raise HTTPException(status_code=quiz_key_request.status_code, detail=load_error_json(quiz_key_request))