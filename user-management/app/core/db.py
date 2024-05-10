from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.core.roles import UserRole
from app.models import User, UserCreate

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

test_connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

# recycle connections after 5 minutes to correspond with the compute scale down
engine = create_engine(connection_string, pool_recycle=300)

tests_engine = create_engine(test_connection_string)


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            role=UserRole.admin,
        )
        user = crud.create_user(session=session, user_create=user_in)
