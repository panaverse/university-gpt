from fastapi import Depends, HTTPException
from typing import Annotated
from sqlmodel import Session

from app.core.db_eng import engine
from app.core import requests
from app.models.topic_models import TopicCreate, TopicUpdate

def get_session():
    with Session(engine) as session:
        yield session

DBSessionDep = Annotated[Session, Depends(get_session)]

def get_course(topic: TopicCreate | TopicUpdate):
    course_request = requests.get_course(topic.course_id)
    return course_request

CourseDep = Annotated[dict, Depends(get_course)]