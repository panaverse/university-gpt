from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker

import pytest
import sys
import os
sys.path.append(os.getcwd())

from app.quiz.question.crud import (add_question, read_questions, read_questions_by_type, get_question_by_id, update_question, delete_question,
                                    add_mcq_option, read_mcq_options, get_mcq_option_by_id, update_mcq_option, delete_mcq_option)
from app.quiz.question.models import QuestionBankCreate, QuestionBankUpdate, MCQOptionCreate, MCQOptionUpdate
from app.quiz.topic.crud import create_topic, delete_topic
from app.quiz.topic.models import TopicCreate

# Load environment variables
load_dotenv(find_dotenv())

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create an asynchronous engine for the database
engine = create_async_engine(DATABASE_URL, echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=3600)

@pytest.fixture(scope="class")
async def async_db_session():
    """Fixture to provide a database session for tests, automatically handling context."""
    async_session = async_sessionmaker(engine, class_ = AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

# Fixture for creating a question
@pytest.fixture(scope="class")
async def new_question(async_db_session):
    async for session in async_db_session:
        # Create topic for the question
        topic = TopicCreate(title="TypeScript", description="TypeScript Programming Language")
        new_topic_created = await create_topic(topic=topic, db=session)

        
        # Create a new question
        question = QuestionBankCreate(
            question_text= "Is Functional Programming same as OOP?",
            is_verified= True,
            points= 1,
            difficulty= "easy",
            topic_id= new_topic_created.id,
            question_type= "single_select_mcq",
            options=[
                MCQOptionCreate(
                    option_text= "Yes",
                    is_correct= True
                ),
                MCQOptionCreate(
                    option_text= "No",
                    is_correct= False
                )
            ]
        )
        new_question_created = await add_question(question=question, db=session)
        yield new_question_created
        await delete_question(id=new_question_created.id, db=session)
        await delete_topic(id=new_topic_created.id, db=session)

class TestQuestionCRUD:
    # @pytest.mark.asyncio
    # async def test_create_new_question(self, async_db_session):
    #     async for session in async_db_session:
    #         # Create topic for the question
    #         topic = TopicCreate(title="TypeScript", description="TypeScript Programming Language")
    #         new_topic_created = await create_topic(topic=topic, db=session)

    #         question = QuestionBankCreate(
    #             question_text= "Is Functional Programming same as OOP?",
    #             is_verified= True,
    #             points= 1,
    #             difficulty= "easy",
    #             topic_id= new_topic_created.id,
    #             question_type= "single_select_mcq",
    #             options=[
    #                 MCQOptionCreate(
    #                     option_text= "Yes",
    #                     is_correct= True
    #                 ),
    #                 MCQOptionCreate(
    #                     option_text= "No",
    #                     is_correct= False
    #                 )
    #             ]
    #         )
    #         new_question = await add_question(question=question, db=session)
    #         assert new_question is not None
    #         assert new_question.id is not None
    #         assert new_question.question_text == question.question_text
    #         assert new_question.is_verified == question.is_verified
    #         assert new_question.points == question.points
    #         assert new_question.difficulty == question.difficulty
    #         assert new_question.topic_id == question.topic_id
    #         assert new_question.question_type == question.question_type
    #         assert new_question.options[0].option_text == question.options[0].option_text
    #         assert new_question.options[0].is_correct == question.options[0].is_correct
    #         assert new_question.options[1].option_text == question.options[1].option_text
    #         assert new_question.options[1].is_correct == question.options[1].is_correct

    #         await delete_question(id=new_question.id, db=session)
    #         await delete_topic(id=new_topic_created.id, db=session)

    # @pytest.mark.asyncio
    # async def test_read_questions(self, async_db_session):
    #     async for session in async_db_session:
    #         questions = await read_questions(db=session, offset=0, limit=10)
    #         assert questions is not None
    #         assert len(questions) >= 0

    @pytest.mark.asyncio
    async def test_get_question_by_id(self, async_db_session, new_question):
        async for session in async_db_session:
            async for mocked_question in new_question:
                question = await get_question_by_id(id=mocked_question.id, db=session)
                assert question is not None
                assert question.id == mocked_question.id
                assert question.question_text == mocked_question.question_text
                assert question.is_verified == mocked_question.is_verified
                assert question.points == mocked_question.points
                assert question.difficulty == mocked_question.difficulty
                assert question.topic_id == mocked_question.topic_id
                assert question.question_type == mocked_question.question_type
                assert question.options[0].option_text == mocked_question.options[0].option_text
                assert question.options[0].is_correct == mocked_question.options[0].is_correct
                assert question.options[1].option_text == mocked_question.options[1].option_text
                assert question.options[1].is_correct == mocked_question.options[1].is_correct

    @pytest.mark.asyncio
    async def test_update_question(self, async_db_session, new_question):
        async for session in async_db_session:
            new_title = "Is Functional Programming same as OOP in Typescript?"
            question_update = QuestionBankUpdate(question_text=new_title, is_verified=False, points=2, difficulty="medium", question_type="single_select_mcq")
            async for mocked_question in new_question:
                updated_question = await update_question(id=mocked_question.id, question=question_update, db=session)
                assert updated_question is not None
                assert updated_question.id == mocked_question.id
                assert updated_question.question_text == new_title
                assert updated_question.is_verified == False
                assert updated_question.points == 2
                assert updated_question.difficulty == "medium"
                assert updated_question.question_type == "single_select_mcq"

    # test read_questions_by_type
    @pytest.mark.asyncio
    async def test_read_questions_by_type(self, async_db_session, new_question):
        async for session in async_db_session:
            async for mocked_question in new_question:
                questions = await read_questions_by_type(question_type=mocked_question.question_type, db=session)
                assert questions is not None
                assert len(questions) >= 0


    # Edge Cases Raising Errors Test
    @pytest.mark.asyncio
    async def test_get_question_by_id_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                question = await get_question_by_id(id=9999999, db=session)

    @pytest.mark.asyncio
    async def test_update_question_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                question_update = QuestionBankUpdate(question_text="", is_verified=False, points=2, difficulty="medium", question_type="single_select_mcq")
                await update_question(id=9999999, question=question_update, db=session)

    @pytest.mark.asyncio
    async def test_delete_question_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                await delete_question(id=9999999, db=session)


class TestMCQOptionCRUD:
    @pytest.mark.asyncio
    async def test_create_new_mcq_option(self, async_db_session, new_question):
        async for session in async_db_session:

            async for mocked_question in new_question:

                mcq_option = MCQOptionCreate(
                    option_text= "Yes",
                    is_correct= True,
                    question_id= mocked_question.id
                )
                new_mcq_option = await add_mcq_option(mcq_option=mcq_option, db=session)
                assert new_mcq_option is not None
                assert new_mcq_option.id is not None
                assert new_mcq_option.option_text == mcq_option.option_text
                assert new_mcq_option.is_correct == mcq_option.is_correct
                assert new_mcq_option.question_id == mcq_option.question_id

    @pytest.mark.asyncio
    async def test_read_mcq_options(self, async_db_session):
        async for session in async_db_session:
            mcq_options = await read_mcq_options(db=session, offset=0, limit=10)
            assert mcq_options is not None
            assert len(mcq_options) >= 0

    @pytest.mark.asyncio
    async def test_get_mcq_option_by_id(self, async_db_session, new_question):
        async for session in async_db_session:
            async for mocked_question in new_question:
                mcq_option = await get_mcq_option_by_id(id=mocked_question.options[0].id, db=session)
                assert mcq_option is not None
                assert mcq_option.id == mocked_question.options[0].id
                assert mcq_option.option_text == mocked_question.options[0].option_text
                assert mcq_option.is_correct == mocked_question.options[0].is_correct
                assert mcq_option.question_id == mocked_question.options[0].question_id

    @pytest.mark.asyncio
    async def test_update_mcq_option(self, async_db_session, new_question):
        async for session in async_db_session:
            new_option_text = "No"
            mcq_option_update = MCQOptionUpdate(option_text=new_option_text, is_correct=False)
            async for mocked_question in new_question:
                updated_mcq_option = await update_mcq_option(id=mocked_question.options[0].id, mcq_option=mcq_option_update, db=session)
                assert updated_mcq_option is not None
                assert updated_mcq_option.id == mocked_question.options[0].id
                assert updated_mcq_option.option_text == new_option_text
                assert updated_mcq_option.is_correct == False

    # Edge Cases Raising Errors Test
    @pytest.mark.asyncio
    async def test_get_mcq_option_by_id_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                mcq_option = await get_mcq_option_by_id(id=9999999, db=session)

    @pytest.mark.asyncio
    async def test_update_mcq_option_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                mcq_option_update = MCQOptionUpdate(option_text="", is_correct=False)
                await update_mcq_option(id=9999999, mcq_option=mcq_option_update, db=session)

    @pytest.mark.asyncio
    async def test_delete_mcq_option_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                await delete_mcq_option(id=9999999, db=session)