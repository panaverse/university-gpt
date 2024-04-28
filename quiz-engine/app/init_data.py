import datetime
from sqlmodel import Session
from app.core.config import logger_config
from app.core.db_eng import engine

from app.models.question_models import QuestionBank
from app.models.answer_models import MCQOption
from app.models.topic_models import Topic
from app.models.content_models import Content
from app.models.quiz_models import Quiz, QuizQuestion
from app.models.quiz_setting import QuizSetting

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


init_topic_name = "Learn Generative AI"
init_course_id = 1

init_sub_topic_name = "Poetry Project Creation"

# Topic & A SubTopic
topic = Topic(
    title=init_topic_name,
    description="""Learn Cloud Applied Generative AI Engineering (GenEng) using OpenAI, Gemini, Streamlit, Containers, Serverless,
              Postgres, LangChain, Pinecone, and Next.js""",
    course_id=init_course_id
)

sub_topic = Topic(
    title= init_sub_topic_name,
    description="Create Project and Manage Dependencies with Poetry",
    parent_id=topic.id,
    parent_topic=topic,
    course_id=init_course_id,
)

sub_topic_content = """Poetry combines dependency management, environment management, and packaging into a single tool.
                  This means you don’t have to juggle between multiple tools like pip, virtualenv, and setuptools."""
# Content
content = Content(
    topic_id=sub_topic.id,
    topic=sub_topic,
    content_text=sub_topic_content
)

# Question Bank & MCQ Options

# QUESTION 1
mcq_option1 = MCQOption(
    option_text="Poetry is a tool for dependency management and packaging in Python.",
    is_correct=True,
)
mcq_option2 = MCQOption(
    option_text="Poetry is a tool for dependency management and packaging in Typescript.",
    is_correct=False,
)
mcq_option3 = MCQOption(
    option_text="Poetry is a tool for dependency management and packaging in Java.",
    is_correct=False,
)
mcq_option4 = MCQOption(
    option_text="Poetry is a tool for dependency management and packaging in C++.",
    is_correct=False,
)

question_bank1 = QuestionBank(
    question_text="What is Poetry?",
    is_verified=True,
    points=1,
    difficulty="easy",
    topic_id=sub_topic.id,
    topic=sub_topic,
    question_type="single_select_mcq",
    options=[mcq_option1, mcq_option2, mcq_option3, mcq_option4],
)

# QUESTION 2
mcq_option2_1 = MCQOption(
    option_text="Management and packaging in Python.", is_correct=True
)
mcq_option2_2 = MCQOption(
    option_text="Virtual Environments Management.", is_correct=True
)
mcq_option2_3 = MCQOption(option_text="Deployment", is_correct=False)
mcq_option2_4 = MCQOption(
    option_text="Dependency management and packaging in C++.", is_correct=False
)

question_bank2 = QuestionBank(
    question_text="Features of Poetry Beneficial for Microservices",
    is_verified=True,
    points=1,
    difficulty="easy",
    topic_id=sub_topic.id,
    topic=sub_topic,
    question_type="multiple_select_mcq",
    options=[mcq_option2_1, mcq_option2_2, mcq_option2_3, mcq_option2_4],
)

# QUESTION 3
mcq_option3_1 = MCQOption(option_text="Use --name Flag", is_correct=True)
mcq_option3_2 = MCQOption(option_text="Not Possible", is_correct=False)
mcq_option3_3 = MCQOption(
    option_text="Create Project & rename Package", is_correct=False
)
mcq_option3_4 = MCQOption(option_text="use --package Flag", is_correct=False)

question_bank3 = QuestionBank(
    question_text="How to create a different package name when creating project using Poetry?",
    is_verified=True,
    points=1,
    difficulty="easy",
    topic_id=sub_topic.id,
    topic=sub_topic,
    question_type="single_select_mcq",
    options=[mcq_option3_1, mcq_option3_2, mcq_option3_3, mcq_option3_4],
)

# Quiz
# quiz_question Instances (This is a Separate COmposite Pattern Table as a Quiz Have Less Topic Questions than in Question Bank)
question_instance_1 = QuizQuestion(
    question_id=question_bank1.id,
    question=question_bank1,
    topic_id=sub_topic.id,
    topic=sub_topic,
)
question_instance_2 = QuizQuestion(
    question_id=question_bank2.id,
    question=question_bank2,
    topic_id=sub_topic.id,
    topic=sub_topic,
)
question_instance_3 = QuizQuestion(
    question_id=question_bank3.id,
    question=question_bank3,
    topic_id=sub_topic.id,
    topic=sub_topic,
)

quiz = Quiz(
    quiz_title="Poetry Quiz",
    difficulty_level="easy",
    random_flag=True,
    total_points=sum(
        [question_bank1.points, question_bank2.points, question_bank3.points]
    ),
    course_id=init_course_id,
    topics=[sub_topic],
    quiz_settings=[],
    quiz_questions=[question_instance_1, question_instance_2, question_instance_3],
)

# Quiz Setting
quiz_setting = QuizSetting(
    quiz_id=quiz.id,
    quiz=quiz,
    instructions="Attempt Carefully",
    time_limit=time_limit_interval,
    start_time=start_time,
    end_time=end_time,
    quiz_key="PoetryQuiz",
)


def init_db_seed(session: Session):
    logger = logger_config(__name__)
    logger.info("RUNNING: init_db_seed Function Up")

     # Topic & A SubTopic
    topic_seed = topic
    session.add(topic_seed)

    sub_topic_seed = sub_topic
    session.add(sub_topic_seed)

    # Content
    content_seed = content
    session.add(content_seed)

    # Question Bank & MCQ Options
    question_bank1_seed = question_bank1
    question_bank2_seed = question_bank2
    question_bank3_seed = question_bank3
    session.add(question_bank1_seed)
    session.add(question_bank2_seed)
    session.add(question_bank3_seed)

    # Quiz
    quiz_seed = quiz
    session.add(quiz_seed)

    # Quiz Setting
    quiz_setting_seed = quiz_setting
    session.add(quiz_setting_seed)

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
                select(Topic).where(Topic.title == init_topic_name)
            )
            topic = topic_req.one_or_none()
            logger.info("\n topic: \n%s\n\n", topic)
            logger.info("\n Checking if Topic is None\n\n")
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
