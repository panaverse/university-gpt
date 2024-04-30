from fastapi import Depends
from typing import Annotated
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.db_eng import engine
from app.core import requests

def get_session():
    with Session(engine) as session:
        yield session

DBSessionDep = Annotated[Session, Depends(get_session)]

def get_course(course_id):
    course_request = requests.get_course(course_id)
    return course_request


CourseDep = Annotated[dict, Depends(get_course)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_student_dep(token: Annotated[str | None, Depends(oauth2_scheme)]):
    user = requests.get_current_user(token)
    return user

GetCurrentStudentDep = Annotated[ str, Depends(get_current_student_dep)]

def get_login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return requests.login_for_access_token(form_data)

LoginForAccessTokenDep = Annotated[dict, Depends(get_login_for_access_token)]