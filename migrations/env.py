import asyncio
from logging.config import fileConfig

from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from dotenv import load_dotenv, find_dotenv
from alembic import context
import os

#from services.quiz.university.models import University, Program, Course
from app.quiz.question.models import QuestionBank, MCQOption
from app.quiz.topic.models import Topic, Content
from app.quiz.university.models import University, Program, Course
from app.quiz.user.models import Student
from app.quiz.quiz.link_models import QuizTopic
from app.quiz.quiz.models import Quiz, QuizQuestion, QuizSetting
from app.quiz.answersheet.models import AnswerSheet, AnswerSlot, AnswerSlotOption

_: bool = load_dotenv(find_dotenv())
DATABASE_URL = "postgresql+asyncpg://todo_owner:ipgcEC0fJd4s@ep-old-block-a5y75062.us-east-2.aws.neon.tech/quiz"
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """    
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())