from fastapi import HTTPException
from requests import get
from app import settings
from app.core.utils import load_error_json

def get_course(course_id: int):
    course_request = get(f"{settings.EDUCATIONAL_PROGRAM_URL}/api/v1/course/{course_id}")
    if course_request.status_code == 200:
        return course_request.json()
    raise HTTPException(status_code=course_request.status_code, detail=load_error_json(course_request))
