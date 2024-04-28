import datetime
from sqlmodel import Session
from app.core.config import logger_config
from app.core.db_eng import engine
from app.models.program_models import Program
from app.models.university_models import University
from app.models.course_models import Course

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

university_name = "PIAIC"
# University
university = University(
    id=1,
    name=university_name,
    description="The University of PIAIC is a leading educational institution in Pakistan.",
)

program_name = "Certified Cloud Applied Generative AI Engineer"
# Program
program = Program(
    name=program_name,
    description="The program of Artificial Intelligence is a leading educational program in Pakistan.",
    university_id=university.id,
    university=university,
)

# Course
course_name = "Quarter 3: API Design, Development, and Deployment using FastAPI, Containers, and OpenAPI Specifications"
course = Course(
    name=course_name,
    description=""" An API-as-a-Product is a type of Software-as-a-Service that monetizes niche functionality, typically served over HTTP.
    OpenAI APIs are themselves this kind of service. An application programming interface economy, or API economy, refers to the business structure
    where APIs are the distribution channel for products and services. In this quarter we will learn to develop APIs not just as a backend for our
    frontend but also as a product itself. In this model, the API is at the core of the business's value. We will be using Python-based FastAPI as
    our core library and Pedantic, SQLAlchemy, and Postgresql databases for API development. Docker Containers will be our fundamental building block
    for development, testing, and deployment. For local development, we will be using Docker Compose and DevPod which is Dev-Environments-As-Code,
    for testing Pytest and Testcontainers, and for deployment Google Cloud Run, Azure Container Service, and Kubernetes. We will be using Terraform
    as our Infrastructure as Code (IaC) tool. OpenAI Chat GPT 4, Google Gemini APIs, and Langchain will be used to build these API-as-a-Product. """,
    program_id=program.id,
    program=program,
)

def init_db_seed(session: Session):
    logger = logger_config(__name__)
    logger.info("Seeding database")

    # University
    university_seed = university
    session.add(university_seed)

    # Program
    program_seed = program
    session.add(program_seed)

    # Course
    course_seed = course
    session.add(course_seed)

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
            university_req = session.exec(
                select(University).where(University.name == university_name)
            )
            university = university_req.one_or_none()
            logger.info("\n University: \n%s\n\n", university)
            logger.info("\n Checking if University is None\n\n")
            if university is None:
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
