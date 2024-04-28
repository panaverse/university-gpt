from fastapi import Depends
from typing import Annotated
from sqlmodel import Session

from app.core.db_eng import engine
from app.core import requests

def get_session():
    with Session(engine) as session:
        yield session

DBSessionDep = Annotated[Session, Depends(get_session)]

def get_course(course_id):
    course_request = requests.get_course()
    return course_request


CourseDep = Annotated[dict, Depends(get_course)]