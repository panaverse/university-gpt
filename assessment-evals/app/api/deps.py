from fastapi import Depends, HTTPException
from typing import Annotated, Any
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.db_eng import engine
from app.core import requests

def get_session():
    with Session(engine) as session:
        yield session

DBSessionDep = Annotated[Session, Depends(get_session)]

#####################
# Dependency Injection for Current Student
#####################

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_student_dep(token: Annotated[str | None, Depends(oauth2_scheme)]):
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = requests.get_current_user(token)
    return user

GetCurrentStudentDep = Annotated[ Any, Depends(get_current_student_dep)]

def get_login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return requests.login_for_access_token(form_data)

LoginForAccessTokenDep = Annotated[dict, Depends(get_login_for_access_token)]

#####################
# Dependency Injection for Current Student
#####################

def get_course(course_id, token: Annotated[str | None, Depends(oauth2_scheme)]):
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    course_request = requests.get_course(course_id, token)
    return course_request


CourseDep = Annotated[dict, Depends(get_course)]