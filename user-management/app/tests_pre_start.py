import logging

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app import crud
from app.core.config import settings
from app.core.db import tests_engine
from app.core.roles import UserRole
from app.models import User, UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


def create_tables(*, db_engine: Engine) -> None:
    # Create ALl TABLES
    # SQLModel.metadata.drop_all(db_engine)
    logger.info("Creating all tables")
    SQLModel.metadata.create_all(db_engine)


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init_test_db(db_engine: Engine) -> None:
    try:
        # Try to create session to check if DB is awake
        logger.info("Checking if DB is awake")
        create_tables(db_engine=db_engine)
        with Session(db_engine) as session:
            session.exec(select(1))

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

    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init_test_db(tests_engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
