from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, SQLModel
import requests

from app.core.db_eng import tests_engine as engine
from app.api.deps import get_session, get_course_for_quiz, get_course, get_current_admin_dep, get_course_by_id
from app.tests_pre_start import init_test_db
from app.main import app
from app.models.topic_models import Topic
from app.models.content_models import Content
from app.models.question_models import QuestionBank
from app.models.answer_models import MCQOption
from app.models.quiz_models import Quiz, QuizQuestion
from app.models.link_models import QuizTopic
from app.models.quiz_setting import QuizSetting
from tests.utils.test_items import mock_course

@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        statement = delete(MCQOption)
        session.exec(statement)
        statement = delete(Content)
        session.exec(statement)
        statement = delete(QuizQuestion)
        session.exec(statement)
        statement = delete(QuizSetting)
        session.exec(statement)
        statement = delete(QuizTopic)
        session.exec(statement)
        statement = delete(QuestionBank)
        session.exec(statement)
        statement = delete(Quiz)
        session.exec(statement)
        statement = delete(Topic)
        session.exec(statement)
        session.commit()
        

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    
    with Session(engine) as session:     
         init_test_db(session=session, db_engine=engine)

    with Session(engine) as session:      
            
        def get_session_override():  
                yield session
                
        def get_course_for_quiz_override():
            return mock_course
        
        def get_admin_overide():
            pass
        
        app.dependency_overrides[get_session] = get_session_override 
        app.dependency_overrides[get_course_for_quiz] = get_course_for_quiz_override 
        app.dependency_overrides[get_course] = get_course_for_quiz_override 
        app.dependency_overrides[get_course_by_id] = get_course_for_quiz_override
        app.dependency_overrides[get_current_admin_dep] = get_admin_overide
        
        with TestClient(app) as c:
            print("Setting up Test Client")
            yield c


# TODO: Add these after additing Authentication to all Routes
# @pytest.fixture(scope="module")
# def superuser_token_headers(client: TestClient) -> dict[str, str]:
#     return get_superuser_token_headers(client)


# @pytest.fixture(scope="module")
# def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
#     return authentication_token_from_email(
#         client=client, email=settings.EMAIL_TEST_USER, db=db
#     )

