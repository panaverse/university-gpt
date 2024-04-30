from sqlalchemy import Engine
from sqlmodel import Session, select, SQLModel

from app.core.db_eng import tests_engine as engine
from app.core.config import logger_config
from app.init_data import init_db_seed

logger = logger_config(__name__)

def create_tables(*, db_engine: Engine) -> None:
    # Create ALl TABLES
    # SQLModel.metadata.drop_all(db_engine)
    logger.info("Creating all tables")
    SQLModel.metadata.create_all(db_engine)

def init_test_db(*, session: Session, db_engine: Engine=engine) -> None:
    try:
        # Try to create session to check if DB is awake
        logger.info("Checking if DB is awake")
        create_tables(db_engine=db_engine)
        logger.info("Seeding the Test DB")
        init_db_seed(session=session)
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    with Session(engine) as session:
        init_test_db(session=session, db_engine=engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()