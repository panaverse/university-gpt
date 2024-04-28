import datetime
from sqlmodel import Session
from app.core.config import logger_config
from app.core.db_eng import engine

from app.models.answersheet_model import AnswerSheet
from app.models.answerslot_model import AnswerSlot

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from sqlmodel import select

logger = logger_config(__name__)

max_tries = 3
wait_seconds = 1

# Calculate the end time based on the start time and the time limit
start_time = datetime.datetime.utcnow()
time_limit_days = 3  # Assuming 3 days for the time limit
time_limit_interval = datetime.timedelta(days=time_limit_days)
end_time = start_time + datetime.timedelta(days=time_limit_days)


# Extract the data outside of the function
logger = logger_config(__name__)
logger.info("Seeding database")

def init_db_seed(session: Session):
    logger = logger_config(__name__)
    logger.info("RUNNING: init_db_seed Function Up")

    session.commit()


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, 200),
    after=after_log(logger, 300),
)
def init_db(*, engine):
    try:
        logger.info("init_db Up")
        with Session(engine) as session:
            logger.info("Checking if Database is already seeded")
            topic_req = session.exec(
                select(AnswerSheet).where(AnswerSheet.id == 1)
            )
            topic = topic_req.one_or_none()
            logger.info("\n topic: \n%s\n\n", topic)
            logger.info("\n Checking if AnswerSheet is None\n\n")
            if topic is None:
                logger.info("Database not seeded. Seeding Database")
                init_db_seed(session=session)
            else:
                logger.info("Database already seeded")
                return {"message": "Database already seeded"}
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    logger.info("In Initial Data Seeding Script")
    (init_db(engine=engine))
    logger.info("Database Seeding Completed!")
    logger.info("Database is Working!")
    logger.info("Backend Database Initial Data Seeding Completed!")
