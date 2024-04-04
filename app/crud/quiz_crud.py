from fastapi import HTTPException, status
from datetime import datetime

from sqlmodel import select, delete, and_
from sqlalchemy.orm import selectinload
from app.core.db import AsyncSession

from app.core.config import logger_config
from app.models.topic_models import Topic
from app.models.quiz_models import (
    Quiz,
    QuizCreate,
    QuizUpdate,
    QuizQuestion,
    QuizSetting,
    QuizSettingCreate,
    QuizSettingUpdate,
)
from app.models.question_models import QuestionBank, QuestionBankCreate, MCQOption

logger = logger_config(__name__)

# -----------------------------
# Quiz Questions
# -----------------------------


class CRUDQuizEngine:
    async def _fetch_all_subtopics(self, *, topic_ids: list[int], db: AsyncSession):
        topics_and_subtopics = await db.exec(
            select(Topic)
            .options(selectinload(Topic.children_topics))  # type:ignore
            .where(Topic.id.in_(topic_ids))  # type:ignore
        )  #
        topics_from_db = topics_and_subtopics.all()

        print("\n---------topics_from_db--------\n", topics_from_db)

        if not topics_from_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incorrect Topic IDs Provided",
            )

        all_topic_data = []
        all_topic_ids = set()

        async def fetch_subtopics(topic_ids):
            nonlocal all_topic_data, all_topic_ids
            topics_result = await db.exec(
                select(Topic)
                .options(selectinload(Topic.children_topics))
                .where(Topic.id.in_(topic_ids))
            )
            topics = topics_result.all()
            # for topic in topics:
            for topic in topics:
                if topic not in all_topic_data:
                    all_topic_data.append(topic)  # Store the topic object
                    all_topic_ids.add(topic.id)  # Store the topic ID
                if topic.children_topics:
                    child_topic_ids = [child.id for child in topic.children_topics]
                    await fetch_subtopics(child_topic_ids)

        await fetch_subtopics(topic_ids)

        return all_topic_ids, all_topic_data

    # Create Quiz
    async def create_quiz(self, *, quiz: QuizCreate, db: AsyncSession):
        try:
            question_ids_with_topics: list = []  # Store tuples of (question_id, topic_id)
            topic_from_db = []

            # Get all topics if topic_ids are provided and append to quiz.topics
            if quiz.add_topic_ids:
                all_topic_ids, all_topic_data = await self._fetch_all_subtopics(
                    topic_ids=quiz.add_topic_ids, db=db
                )

                print("\n----all_topic_ids----\n", all_topic_ids)

                # Fetch all unique questions linked to these topics and subtopics
                questions_result = await db.exec(
                    select(QuestionBank.id, QuestionBank.topic_id).where(
                        QuestionBank.topic_id.in_(all_topic_ids),  # type:ignore
                        QuestionBank.is_verified == True,
                    )
                )  # type:ignore

                all_questions = questions_result.all()

                print(
                    "\n----questions_result----\n",
                    questions_result,
                    "\n\n\n",
                    all_questions,
                )

                question_ids_with_topics.extend(all_questions)

                print(
                    "\n\n\n----question_ids_with_topics----\n\n\n",
                    question_ids_with_topics,
                )

                # Append the topics to the quiz
                topic_from_db.extend(all_topic_data)

                print("\n----TOPICS_FROM_DB----\n", topic_from_db)

            quiz_to_db = Quiz.model_validate(quiz)
            quiz_to_db.topics = topic_from_db
            db.add(quiz_to_db)
            await db.commit()
            await db.refresh(quiz_to_db)

            if question_ids_with_topics:
                quiz_questions_instances = [
                    QuizQuestion(quiz_id=quiz_to_db.id, question_id=q_id, topic_id=t_id)
                    for q_id, t_id in question_ids_with_topics
                ]
                print("\n----quiz_questions_instances----\n", quiz_questions_instances)
                db.add_all(quiz_questions_instances)

            await db.commit()
            # await db.refresh(quiz_to_db)

            print("\n----quiz_to_db----\n", quiz_to_db)
            print("\n----quiz_to_db.id----\n", quiz_to_db.id)

            # Fetch the quiz with the topics and questions
            quiz_added = await self.read_quiz_by_id(quiz_id=quiz_to_db.id, db=db)  # type:ignore

            print("\n----quiz_added.total_points----\n", quiz_added.total_points)

            # Update quiz points - based on the sum of all question points
            quiz_added.total_points = sum(
                [
                    quiz_question.question.points
                    for quiz_question in quiz_added.quiz_questions
                ]
            )
            print("\n----quiz_added.total_points----\n", quiz_added.total_points)

            await db.commit()
            # await db.refresh(quiz_added)

            return quiz_added

        except HTTPException as http_err:
            await db.rollback()
            logger.error(f"create_quiz Error: {http_err}")
            raise http_err

        except Exception as e:
            await db.rollback()
            logger.error(f"create_quiz Error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def read_all_quizzes_for_course(
        self, *, db: AsyncSession, course_id: int, offset: int, limit: int
    ):
        try:
            result = await db.exec(
                select(Quiz)
                .options(selectinload(Quiz.topics))  # type:ignore
                .where(Quiz.course_id == course_id)
                .offset(offset)
                .limit(limit)
            )
            quizzes = result.all()
            if not quizzes:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Quizzes not found"
                )
            return quizzes
        except HTTPException as e:
            await db.rollback()
            logger.error(f"read_all_quizzes Error: {e}")
            raise e
        except Exception as e:
            await db.rollback()
            logger.error(f"read_all_quizzes Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in fetching Quizzes",
            )

    async def read_quiz_by_id(self, *, quiz_id: int, db: AsyncSession):
        try:
            # quiz = await db.get(Quiz, quiz_id)
            result = await db.exec(
                select(Quiz)
                .options(
                    selectinload(Quiz.topics),  # type:ignore
                    selectinload(Quiz.quiz_settings),  # type:ignore
                    selectinload(
                        Quiz.quiz_questions  # type:ignore
                    ).joinedload(QuizQuestion.question),  # type:ignore
                )
                .where(Quiz.id == quiz_id)  # type:ignore
            )
            quiz = result.one()
            if not quiz:
                raise ValueError("Quiz not found")
            return quiz
        except ValueError as e:
            await db.rollback()
            logger.error(f"read_quiz Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"read_quiz Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quiz"
            )

    async def _add_new_topics(
        self, quiz_to_update, new_topic_ids, existing_topic_ids, db
    ):
        newly_added_topic_ids = set()
        if new_topic_ids:
            new_topics_with_subtopics = await db.exec(
                select(Topic)
                .options(selectinload(Topic.children_topics))
                .where(Topic.id.in_(new_topic_ids))
            )
            for topic in new_topics_with_subtopics.all():
                if topic.id not in existing_topic_ids:
                    quiz_to_update.topics.append(topic)
                    newly_added_topic_ids.add(topic.id)
                for child in topic.children_topics:
                    if (
                        child.id not in existing_topic_ids
                        and child.id not in new_topic_ids
                    ):
                        quiz_to_update.topics.append(child)
                        newly_added_topic_ids.add(child.id)
            await db.commit()
        return newly_added_topic_ids

    async def _add_new_questions(self, quiz_id, newly_added_topic_ids, db):
        if newly_added_topic_ids:
            questions_result = await db.execute(
                select(QuestionBank).where(
                    QuestionBank.topic_id.in_(list(newly_added_topic_ids)),
                    QuestionBank.is_verified == True,
                )
            )
            questions_to_add = questions_result.all()
            new_quiz_questions = [
                QuizQuestion(
                    quiz_id=quiz_id, question_id=question.id, topic_id=question.topic_id
                )
                for question in questions_to_add
            ]
            db.add_all(new_quiz_questions)
            await db.commit()

    async def _remove_topics(self, quiz_to_update, topics_to_remove, db):
        if topics_to_remove:
            # 1. Remove QuizTopic Link
            quiz_to_update.topics = [
                topic
                for topic in quiz_to_update.topics
                if topic.id not in topics_to_remove
            ]
            # 2. Remove QuizQuestion Link
            await db.execute(
                delete(QuizQuestion).where(
                    QuizQuestion.question_id.in_(
                        select(QuestionBank.id).where(
                            QuestionBank.topic_id.in_(topics_to_remove)
                        )
                    ),
                    QuizQuestion.quiz_id == quiz_to_update.id,
                )
            )
            await db.commit()

    async def update_quiz(
        self, *, quiz_id: int, quiz_update_data: QuizUpdate, db: AsyncSession
    ):
        try:
            quiz_to_update = await self.read_quiz_by_id(quiz_id=quiz_id, db=db)

            existing_topic_ids = {topic.id for topic in quiz_to_update.topics}
            new_topic_ids = (
                set(quiz_update_data.add_topic_ids) - existing_topic_ids
                if quiz_update_data.add_topic_ids
                else set()
            )
            topics_to_remove = (
                set(quiz_update_data.remove_topic_ids)
                if quiz_update_data.remove_topic_ids
                else set()
            )

            newly_added_topic_ids = await self._add_new_topics(
                quiz_to_update, new_topic_ids, existing_topic_ids, db
            )
            await self._add_new_questions(quiz_id, newly_added_topic_ids, db)
            await self._remove_topics(quiz_to_update, topics_to_remove, db)

            for key, value in quiz_update_data.model_dump(exclude_unset=True).items():
                if hasattr(quiz_to_update, key):
                    setattr(quiz_to_update, key, value)

            await db.commit()
            db.expire_all()

            quiz_updated = await self.read_quiz_by_id(quiz_id=quiz_id, db=db)
            quiz_updated.total_points = sum(
                quiz_question_link.question.points
                for quiz_question_link in quiz_updated.quiz_questions
            )
            await db.commit()

            return quiz_updated
        except HTTPException:
            await db.rollback()
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"update_quiz Error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def delete_quiz(self, *, quiz_id: int, db: AsyncSession):
        try:
            print("\n----quiz_id----\n", quiz_id)
            quiz_to_delete = await db.get(Quiz, quiz_id)

            if not quiz_to_delete:
                raise ValueError("Quiz not found")

            print("\n----quiz_to_delete----\n", quiz_to_delete)

            logger.info(f"DELETE_QUIZ_TEST: {quiz_to_delete}")

            await db.delete(quiz_to_delete)
            await db.commit()

            return {"message": "Quiz deleted successfully!"}
        except ValueError as e:
            await db.rollback()
            logger.error(f"delete_quiz Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"delete_quiz Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Error in deleting Quiz"
            )


# -----------------------------
# Quiz Questions
# -----------------------------


class CRUDQuizQuestion:
    # 1. Create Quiz Question
    async def create_quiz_question(
        self,
        *,
        quiz_id: int,
        quiz_question_create_data: QuestionBankCreate,
        db: AsyncSession,
    ):
        try:
            # 0. If quiz_question_create_data.is_verified is False Raise Error
            if not quiz_question_create_data.is_verified:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Question must be verified as True to be added in Quiz",
                )
            # 1. Get the quiz to link the question to
            quiz = await db.get(Quiz, quiz_id)
            if not quiz:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
                )

            # 2. Add Question to the QuestionBank then link to the Quiz using QuizQuestion Model
            if quiz_question_create_data.options:
                quiz_question_create_data.options = [
                    MCQOption.model_validate(option)  # type:ignore
                    for option in quiz_question_create_data.options
                ]  # type:ignore

            question_to_db = QuestionBank.model_validate(quiz_question_create_data)

            quiz_question_link = QuizQuestion(
                quiz=quiz, question=question_to_db, topic_id=question_to_db.topic_id
            )

            db.add(quiz_question_link)
            await db.commit()
            await db.refresh(quiz_question_link)

            return quiz_question_link

        except Exception as e:
            await db.rollback()
            logger.error(f"create_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in creating Quiz Question",
            )

    # Remove a Quiz Question
    async def remove_quiz_question(
        self, *, quiz_id: int, quiz_question_id: int, db: AsyncSession
    ):
        try:
            query = select(QuizQuestion).where(
                and_(
                    QuizQuestion.quiz_id == quiz_id,
                    QuizQuestion.question_id == quiz_question_id,
                )
            )
            quiz_question_row = await db.exec(query)
            quiz_question_instance = quiz_question_row.one_or_none()
            print("\n----quiz_question_to_delete----\n", quiz_question_instance)
            if not quiz_question_instance:
                raise ValueError("Quiz Question not found")
            # for quiz_question in quiz_question_instance:

            await db.delete(quiz_question_instance)
            await db.commit()
            return {"message": "Quiz Question deleted successfully!"}
        except ValueError as e:
            await db.rollback()
            logger.error(f"remove_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question not found"
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"remove_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in deleting Quiz Question",
            )

    # Rest can be done directly via QUestions Crud API as this is just a link between Quiz and QuestionBank


# -------------------------------------------
#             # QuizSetting CRUD
# -------------------------------------------
class CRUDQuizSetting:
    async def create_quiz_setting(
        self, *, db: AsyncSession, quiz_setting: QuizSettingCreate
    ):
        """
        Create a new QuizSetting in the database
        """
        # Create a new QuizSetting
        # Convert start_time and end_time to offset-naive datetime objects if they are not None
        if quiz_setting.start_time and quiz_setting.start_time.tzinfo:
            quiz_setting.start_time = quiz_setting.start_time.replace(tzinfo=None)

        if quiz_setting.end_time and quiz_setting.end_time.tzinfo:
            quiz_setting.end_time = quiz_setting.end_time.replace(tzinfo=None)

        db_quiz_setting = QuizSetting.model_validate(quiz_setting)

        print("\n----db_quiz_setting----\n", db_quiz_setting)

        # Add the new QuizSetting to the database
        db.add(db_quiz_setting)

        # Commit the session to the database to actually add the QuizSetting
        await db.commit()

        # Refresh the database to get the updated details of the QuizSetting
        await db.refresh(db_quiz_setting)

        # Return the newly created QuizSetting
        return db_quiz_setting

    # Get all QuizSettings for a quiz
    async def get_all_quiz_settings_for_quiz(self, *, db: AsyncSession, quiz_id: int):
        """
        Get all QuizSettings from the database
        """
        try:
            quiz_settings = await db.exec(
                select(QuizSetting).where(and_(QuizSetting.quiz_id == quiz_id))
            )
            # Return all QuizSettings
            return quiz_settings.all()

        except Exception as e:
            await db.rollback()
            logger.error(f"get_all_quiz_settings_for_quiz Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Get a QuizSetting by ID
    async def get_quiz_setting_by_id(
        self, *, db: AsyncSession, quiz_setting_id: int
    ) -> QuizSetting:
        """
        Get a QuizSetting from the database by ID
        """
        try:
            quiz_setting = await db.get(QuizSetting, quiz_setting_id)

            # If the QuizSetting doesn't exist, raise an HTTPException
            if quiz_setting is None:
                raise HTTPException(status_code=404, detail="QuizSetting not found")

            # Return the QuizSetting
            return quiz_setting
        except Exception as e:
            await db.rollback()
            logger.error(f"get_quiz_setting_by_id Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Update a QuizSetting
    async def update_quiz_setting(
        self,
        *,
        db: AsyncSession,
        quiz_setting_id: int,
        quiz_setting_update: QuizSettingUpdate,
    ) -> QuizSetting:
        """
        Update a QuizSetting in the database
        """
        try:
            db_quiz_setting = await db.get(QuizSetting, quiz_setting_id)

            if db_quiz_setting is None:
                raise HTTPException(status_code=404, detail="QuizSetting not found")

            update_data = quiz_setting_update.model_dump(exclude_unset=True)

            db_quiz_setting.sqlmodel_update(update_data)

            await db.commit()
            await db.refresh(db_quiz_setting)
            return db_quiz_setting
        except Exception as e:
            await db.rollback()
            logger.error(f"update_quiz_setting Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Remove a QUiz Setting
    async def remove_quiz_setting(
        self, *, db: AsyncSession, quiz_setting_id: int
    ) -> dict:
        """
        Remove a QuizSetting from the database
        """
        try:
            db_quiz_setting = await db.get(QuizSetting, quiz_setting_id)

            if db_quiz_setting is None:
                raise HTTPException(status_code=404, detail="QuizSetting not found")

            await db.delete(db_quiz_setting)
            await db.commit()
            return {"message": "QuizSetting deleted successfully!"}
        except Exception as e:
            await db.rollback()
            logger.error(f"remove_quiz_setting Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Check Is Key Valid
    async def validate_quiz_key(self, *, db: AsyncSession, quiz_id: int, quiz_key: str):
        """
        Check if the Quiz Key is valid
        """
        try:
            quiz_setting_statement = await db.exec(
                select(QuizSetting).where(
                    and_(
                        QuizSetting.quiz_id == quiz_id, QuizSetting.quiz_key == quiz_key
                    )
                )
            )
            quiz_setting = quiz_setting_statement.one_or_none()

            if quiz_setting is None:
                raise HTTPException(status_code=404, detail="QuizSetting not found")

            # If Time is not None then check if it is between start and end time
            if quiz_setting.start_time and quiz_setting.end_time:
                if (
                    not quiz_setting.start_time
                    <= datetime.now()
                    <= quiz_setting.end_time
                ):
                    raise HTTPException(status_code=404, detail="Quiz is not active")

            return quiz_setting
        except HTTPException as httperr:
            await db.rollback()
            logger.error(f"is_quiz_key_valid Error: {httperr}")
            raise httperr
        except Exception as e:
            await db.rollback()
            logger.error(f"is_quiz_key_valid Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))


# ------------------------------
# Quiz Generation Endpoint
# ------------------------------


class QuizRuntimeEngine:
    async def generate_quiz(self, *, quiz_id: int, db: AsyncSession):
        try:
            # 1. Verify Student ID
            # student = await db.get(Student, student_id)
            # if not student:
            #     raise HTTPException(
            #         status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
            #     )

            # 2. Verify Quiz ID and Quiz Key
            quiz_with_question_result = await db.exec(
                select(Quiz)
                .options(
                    selectinload(Quiz.quiz_questions).joinedload(QuizQuestion.question)  # type:ignore  # type:ignore
                )
                .where(Quiz.id == quiz_id)
            )
            quiz_with_questions = quiz_with_question_result.one()

            if not quiz_with_questions:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
                )

            # 5. Return Quiz with Questions
            return quiz_with_questions

        except HTTPException as e:
            await db.rollback()
            logger.error(f"generate_quiz Error: {e}")
            raise e
        except Exception as e:
            await db.rollback()
            logger.error(f"generate_quiz Error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Initalize all the CRUD Classes
quiz_engine = CRUDQuizEngine()
quiz_question_engine = CRUDQuizQuestion()
quiz_setting_engine = CRUDQuizSetting()
runtime_quiz_engine = QuizRuntimeEngine()
