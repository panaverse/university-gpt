from fastapi import Depends, HTTPException
from typing import Annotated
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.db_eng import engine
from app.core import requests
from app.models.topic_models import TopicCreate, TopicUpdate
from app.models.quiz_models import QuizCreate

def get_session():
    with Session(engine) as session:
        yield session

DBSessionDep = Annotated[Session, Depends(get_session)]

###########################
# Auth Deps
###########################

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_admin_dep(token: Annotated[str | None, Depends(oauth2_scheme)]):
    user = requests.get_current_user(token)
    if user.get("is_superuser") == False:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

GetCurrentAdminDep = Depends(get_current_admin_dep)

def get_login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth_tokens = requests.login_for_access_token(form_data)
    # Make a request to get user data and check if user is admin
    user = requests.get_current_user(auth_tokens.get("access_token"))
    if user.get("is_superuser") == False:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return auth_tokens

LoginForAccessTokenDep = Annotated[dict, Depends(get_login_for_access_token)]


###########################
# Course Deps
###########################


def get_course(topic: TopicCreate | TopicUpdate, token: Annotated[str | None, Depends(oauth2_scheme)]):
    course_request = requests.get_course(topic.course_id, token)
    return course_request

def get_course_for_quiz(quiz: QuizCreate, token: Annotated[str | None, Depends(oauth2_scheme)]):
    course_request = requests.get_course(quiz.course_id, token)
    return course_request

def get_course_by_id(course_id: int, token: Annotated[str | None, Depends(oauth2_scheme)]):
    course_request = requests.get_course(course_id, token)
    return course_request

CourseDep = Annotated[dict, Depends(get_course)]

CourseQuizDep = Annotated[dict, Depends(get_course_for_quiz)]

CourseByIdDep = Annotated[dict, Depends(get_course_by_id)]