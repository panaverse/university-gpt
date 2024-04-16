import pytest
from app.pre_start_tests import TestAsyncSessionLocal

from app.models.question_models import (
    QuestionBankCreate,
    QuestionBankUpdate,
    MCQOptionCreate,
    MCQOptionUpdate,
)
from app.crud.question_crud import question_crud, mcq_crud
from app.crud.topic_crud import topic_crud
from app.models.topic_models import TopicCreate


@pytest.fixture(scope="class")
async def async_db_session():
    """Fixture to provide a database session for tests, automatically handling context."""
    async with TestAsyncSessionLocal() as session:
        yield session


# Fixture for creating a question
@pytest.fixture(scope="class")
async def new_question(async_db_session):
    async for session in async_db_session:
        # Create topic for the question
        topic = TopicCreate(
            title="TypeScript", description="TypeScript Programming Language"
        )
        new_topic_created = await topic_crud.create_topic(topic=topic, db=session)

        # Create a new question
        question = QuestionBankCreate(
            question_text="Is Functional Programming same as OOP?",
            is_verified=True,
            points=1,
            difficulty="easy",
            topic_id=new_topic_created.id,
            question_type="single_select_mcq",
            options=[
                MCQOptionCreate(option_text="Yes", is_correct=True),
                MCQOptionCreate(option_text="No", is_correct=False),
            ],
        )
        new_question_created = await question_crud.add_question(
            question=question, db=session
        )
        yield new_question_created
        await question_crud.delete_question(id=new_question_created.id, db=session)
        await topic_crud.delete_topic(id=new_topic_created.id, db=session)


class TestQuestionCRUD:
    @pytest.mark.asyncio
    async def test_read_questions(self, async_db_session):
        async for session in async_db_session:
            questions = await question_crud.read_questions(
                db=session, offset=0, limit=10
            )
            assert questions is not None
            assert len(questions) >= 0

    @pytest.mark.asyncio
    async def test_get_question_by_id(self, async_db_session, new_question):
        async for session in async_db_session:
            async for mocked_question in new_question:
                question = await question_crud.get_question_by_id(
                    id=mocked_question.id, db=session
                )
                assert question is not None
                assert question.id == mocked_question.id
                assert question.question_text == mocked_question.question_text
                assert question.is_verified == mocked_question.is_verified
                assert question.points == mocked_question.points
                assert question.difficulty == mocked_question.difficulty
                assert question.topic_id == mocked_question.topic_id
                assert question.question_type == mocked_question.question_type
                assert (
                    question.options[0].option_text
                    == mocked_question.options[0].option_text
                )
                assert (
                    question.options[0].is_correct
                    == mocked_question.options[0].is_correct
                )
                assert (
                    question.options[1].option_text
                    == mocked_question.options[1].option_text
                )
                assert (
                    question.options[1].is_correct
                    == mocked_question.options[1].is_correct
                )

    @pytest.mark.asyncio
    async def test_update_question(self, async_db_session, new_question):
        async for session in async_db_session:
            new_title = "Is Functional Programming same as OOP in Typescript?"
            question_update = QuestionBankUpdate(
                question_text=new_title,
                is_verified=False,
                points=2,
                difficulty="medium",
                question_type="single_select_mcq",
            )
            async for mocked_question in new_question:
                updated_question = await question_crud.update_question(
                    id=mocked_question.id, question=question_update, db=session
                )
                assert updated_question is not None
                assert updated_question.id == mocked_question.id
                assert updated_question.question_text == new_title
                assert updated_question.is_verified is False
                assert updated_question.points == 2
                assert updated_question.difficulty == "medium"
                assert updated_question.question_type == "single_select_mcq"

    # test read_questions_by_type
    @pytest.mark.asyncio
    async def test_read_questions_by_type(self, async_db_session, new_question):
        async for session in async_db_session:
            async for mocked_question in new_question:
                questions = await question_crud.read_questions_by_type(
                    question_type=mocked_question.question_type, db=session
                )
                assert questions is not None
                assert len(questions) >= 0

    # Edge Cases Raising Errors Test
    @pytest.mark.asyncio
    async def test_get_question_by_id_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                await question_crud.get_question_by_id(id=9999999, db=session)

    @pytest.mark.asyncio
    async def test_update_question_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                question_update = QuestionBankUpdate(
                    question_text="",
                    is_verified=False,
                    points=2,
                    difficulty="medium",
                    question_type="single_select_mcq",
                )
                await question_crud.update_question(
                    id=9999999, question=question_update, db=session
                )

    @pytest.mark.asyncio
    async def test_delete_question_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                await question_crud.delete_question(id=9999999, db=session)


class TestMCQOptionCRUD:
    @pytest.mark.asyncio
    async def test_create_new_mcq_option(self, async_db_session, new_question):
        async for session in async_db_session:
            async for mocked_question in new_question:
                mcq_option = MCQOptionCreate(
                    option_text="Yes", is_correct=True, question_id=mocked_question.id
                )
                new_mcq_option = await mcq_crud.add_mcq_option(
                    mcq_option=mcq_option, db=session
                )
                assert new_mcq_option is not None
                assert new_mcq_option.id is not None
                assert new_mcq_option.option_text == mcq_option.option_text
                assert new_mcq_option.is_correct == mcq_option.is_correct
                assert new_mcq_option.question_id == mcq_option.question_id

    @pytest.mark.asyncio
    async def test_read_mcq_options(self, async_db_session):
        async for session in async_db_session:
            mcq_options = await mcq_crud.read_mcq_options(
                db=session, offset=0, limit=10
            )
            assert mcq_options is not None
            assert len(mcq_options) >= 0

    @pytest.mark.asyncio
    async def test_get_mcq_option_by_id(self, async_db_session, new_question):
        async for session in async_db_session:
            async for mocked_question in new_question:
                mcq_option = await mcq_crud.get_mcq_option_by_id(
                    id=mocked_question.options[0].id, db=session
                )
                assert mcq_option is not None
                assert mcq_option.id == mocked_question.options[0].id
                assert mcq_option.option_text == mocked_question.options[0].option_text
                assert mcq_option.is_correct == mocked_question.options[0].is_correct
                assert mcq_option.question_id == mocked_question.options[0].question_id

    @pytest.mark.asyncio
    async def test_update_mcq_option(self, async_db_session, new_question):
        async for session in async_db_session:
            new_option_text = "No"
            mcq_option_update = MCQOptionUpdate(
                option_text=new_option_text, is_correct=False
            )
            async for mocked_question in new_question:
                updated_mcq_option = await mcq_crud.update_mcq_option(
                    id=mocked_question.options[0].id,
                    mcq_option=mcq_option_update,
                    db=session,
                )
                assert updated_mcq_option is not None
                assert updated_mcq_option.id == mocked_question.options[0].id
                assert updated_mcq_option.option_text == new_option_text
                assert updated_mcq_option.is_correct is False

    # Edge Cases Raising Errors Test
    @pytest.mark.asyncio
    async def test_get_mcq_option_by_id_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                await mcq_crud.get_mcq_option_by_id(id=9999999, db=session)

    @pytest.mark.asyncio
    async def test_update_mcq_option_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                mcq_option_update = MCQOptionUpdate(option_text="", is_correct=False)
                await mcq_crud.update_mcq_option(
                    id=9999999, mcq_option=mcq_option_update, db=session
                )

    @pytest.mark.asyncio
    async def test_delete_mcq_option_value_error(self, async_db_session):
        async for session in async_db_session:
            with pytest.raises(ValueError):
                await mcq_crud.delete_mcq_option(id=9999999, db=session)
