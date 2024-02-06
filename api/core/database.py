from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import OperationalError

from api.config import settings

engine = create_engine(settings.DATABASE_URI, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session

# Dependency with retry mechanism for OperationalError
def get_session():
        db = Session(engine)
        try:
            yield db
        except OperationalError as e:
            print(f"SSL connection error occurred: {e}, retrying...")
        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
        finally:
            db.close()