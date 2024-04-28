from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.db_eng import tests_engine as engine
from app.api.deps import get_session
from app.tests_pre_start import init_test_db
from app.main import app
from app.models.course_models import Course
from app.models.program_models import Program
from app.models.university_models import University

@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        statement = delete(Course)
        session.exec(statement)
        statement = delete(Program)
        session.exec(statement)
        statement = delete(University)
        session.exec(statement)
        session.commit()

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    
    with Session(engine) as session:     
         init_test_db(session=session, db_engine=engine)

    with Session(engine) as session:      
            
        def get_session_override():  
                yield session
        
        app.dependency_overrides[get_session] = get_session_override 
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