from sqlmodel import create_engine
from app import settings

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

test_connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

# recycle connections after 5 minutes to correspond with the compute scale down
engine = create_engine(connection_string, pool_recycle=300)

tests_engine = create_engine(test_connection_string)
