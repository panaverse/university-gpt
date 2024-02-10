from fastapi import HTTPException, status

from sqlmodel import select, and_, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.core.utils.logger import logger_config
from api.quiz.topic.models import Topic
from api.quiz.question.models import QuestionBank, QuestionBankCreate, MCQOption
from api.quiz.quiz.models import (Quiz, QuizCreate, QuizUpdate,
                                  QuizUpdate, QuizQuestion, QuizQuestionUpdate)

logger = logger_config(__name__)

# Create Quiz


async def create_quiz(quiz: QuizCreate, db: AsyncSession):
    try:

        # Validate Any New Topics
        if quiz.topics:
            quiz.topics = [Topic.model_validate(
                new_topic) for new_topic in quiz.topics]

        # Get all topics if topic_ids are provided and append to quiz.topics
        if quiz.topic_ids:
            result = await db.execute(select(Topic).where(Topic.id.in_(quiz.topic_ids)))
            topics = result.scalars().all()
            if not topics:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="All Incorrect Topic Ids Provided")
            quiz.topics.extend(topics)

        quiz_to_db = Quiz.model_validate(quiz)

        db.add(quiz_to_db)
        await db.commit()
        db.refresh(quiz_to_db)

        # Associate questions with the quiz based on provided topic_ids
        # TODO: Topics are recusrisve, so we need to update to get questions for subtopics
        for topic_id in quiz.topic_ids:
            questions_result = await db.execute(select(QuestionBank).where(QuestionBank.topic_id == topic_id))
            questions = questions_result.scalars().all()
            for question in questions:
                # Create QuizQuestion link instances for each question
                quiz_question = QuizQuestion(
                    quiz_id=quiz_to_db.id, question_id=question.id)
                db.add(quiz_question)

        await db.commit()

        return quiz_to_db

    except HTTPException as http_err:
        await db.rollback()
        logger.error(f"create_quiz Error: {http_err}")
        raise http_err

    except IntegrityError as e:
        await db.rollback()
        logger.error(f"create_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz Already Exists")

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"create_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz")

    except Exception as e:
        await db.rollback()
        logger.error(f"create_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz")


async def read_all_quizzes(db: AsyncSession, offset: int, limit: int):
    try:
        result = await db.execute(select(Quiz).options(selectinload(Quiz.topics)).offset(offset).limit(limit))
        quizzes = result.scalars().all()
        if not quizzes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quizzes not found")
        return quizzes
    except HTTPException as e:
        await db.rollback()
        logger.error(f"read_all_quizzes Error: {e}")
        raise e
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"read_all_quizzes Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quizzes")
    except Exception as e:
        await db.rollback()
        logger.error(f"read_all_quizzes Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quizzes")


async def read_quiz_by_id(quiz_id: int, db: AsyncSession):
    try:
        # quiz = await db.get(Quiz, quiz_id)
        result = await db.execute(
            select(Quiz).options(selectinload(Quiz.topics), selectinload(
                Quiz.quiz_questions).joinedload(QuizQuestion.question)).where(Quiz.id == quiz_id)
        )
        quiz = result.scalars().one()
        if not quiz:
            raise ValueError("Quiz not found")
        return quiz
    except ValueError as e:
        await db.rollback()
        logger.error(f"read_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"read_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quiz")
    except Exception as e:
        await db.rollback()
        logger.error(f"read_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quiz")


async def update_quiz(quiz_id: int, quiz_update_data: QuizUpdate, db: AsyncSession):

    try:
        quiz_to_update = await read_quiz_by_id(quiz_id, db)

        # Validate Any New Topics Ids and Append to quiz.topics if valid
        if quiz_update_data.add_topic_ids:
            result = await db.execute(select(Topic).where(Topic.id.in_(quiz_update_data.add_topic_ids)))
            topics_to_add = result.scalars().all()
            if not topics_to_add:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="All Incorrect Topic Ids Provided")
            # It's safer to use a set to avoid duplicates
            current_topic_ids = {topic.id for topic in quiz_to_update.topics}
            for topic in topics_to_add:
                if topic.id not in current_topic_ids:
                    quiz_to_update.topics.append(topic)

        # Update Quiz Data Fields
        for key, value in quiz_update_data.model_dump(exclude_unset=True, exclude={"add_topic_ids", "remove_topic_ids"}).items():
            setattr(quiz_to_update, key, value)

        db.add(quiz_to_update)

        await db.commit()  # Commit quiz updates

        # Add new questions to the quiz based on the new topic Ids
        if quiz_update_data.add_topic_ids:
            # Query all questions linked to the new topics in one go
            questions_result = await db.execute(select(QuestionBank).where(QuestionBank.topic_id.in_(quiz_update_data.add_topic_ids)))
            all_questions = questions_result.scalars().all()
            
            # Loop through the results to create QuizQuestion link instances
            quiz_questions_to_add = [QuizQuestion(quiz_id=quiz_to_update.id, question_id=question.id) for question in all_questions]

            # Add all new QuizQuestion instances to the session
            db.add_all(quiz_questions_to_add)

            await db.commit()

        # Remove topics from the quiz and associated questions from QuizQuestion table if remove_topic_ids are provided
        if quiz_update_data.remove_topic_ids:
            # Remove topics from the quiz
            quiz_to_update.topics = [topic for topic in quiz_to_update.topics if topic.id not in quiz_update_data.remove_topic_ids]

            # Remove Linked Topic Questions from the Quiz
            # First, find all questions linked to these topics
            questions_to_remove_result = await db.execute(
                select(QuestionBank.id)
                .where(QuestionBank.topic_id.in_(quiz_update_data.remove_topic_ids))
            )
            question_ids_to_remove = questions_to_remove_result.scalars().all()

            if question_ids_to_remove:
                # Construct the delete statement for QuizQuestion and Execute it
                await db.execute(delete(QuizQuestion).where(
                    and_(
                        QuizQuestion.question_id.in_(question_ids_to_remove),
                        QuizQuestion.quiz_id == quiz_id
                    )
                ))
                # Commit the changes to the database
                await db.commit()


        db.refresh(quiz_to_update)
        db.expire_all()  # Invalidate all session data
        quiz_to_update = await read_quiz_by_id(quiz_id, db)  # Re-fetch the quiz

        return quiz_to_update

    except HTTPException as http_err:
        logger.error(f"HTTPException update_quiz Error: {http_err}")
        await db.rollback()
        raise http_err
    except IntegrityError as e:
        logger.error(f"IntegrityError update_quiz Error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz Already Exists")
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemyError update_quiz Error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in updating Quiz")
    except Exception as e:
        logger.error(f"Exception update_quiz Error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in updating Quiz")


async def delete_quiz(quiz_id: int, db: AsyncSession):
    try:
        quiz_to_delete = await db.get(Quiz, quiz_id)
        if not quiz_to_delete:
            raise ValueError("Quiz not found")
        logger.info(f"DELETE_QUIZ_TEST: {quiz_to_delete}")
        await db.delete(quiz_to_delete)
        await db.commit()
        return {"message": "Quiz deleted successfully!"}
    except ValueError as e:
        await db.rollback()
        logger.error(f"delete_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"delete_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in deleting Quiz")
    except Exception as e:
        await db.rollback()
        logger.error(f"delete_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in deleting Quiz")

# -----------------------------
# Quiz Questions
# -----------------------------
    
# 1. Create Quiz Question
async def create_quiz_question(quiz_id: int, quiz_question_create_data: QuestionBankCreate, db: AsyncSession):
    try:
        # 1. Get the quiz to link the question to
        quiz = await db.get(Quiz, quiz_id)
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
        
        # 2. Add Question to the QuestionBank then link to the Quiz using QuizQuestion Model
        if quiz_question_create_data.options:
            quiz_question_create_data.options = [MCQOption.model_validate(option) for option in quiz_question_create_data.options]

        question_to_db = QuestionBank.model_validate(quiz_question_create_data)

        quiz_question_link = QuizQuestion(quiz=quiz, question=question_to_db)

        db.add(quiz_question_link)
        await db.commit()
        db.refresh(quiz_question_link)

        return quiz_question_link
    
    except HTTPException as e:
        await db.rollback()
        logger.error(f"create_quiz_question Error: {e}")
        raise e
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"create_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz Question Already Exists")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"create_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz Question")
    except Exception as e:
        await db.rollback()
        logger.error(f"create_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz Question")

# Mute Quiz Question 
async def mute_quiz_question(quiz_id: int, quiz_question_id: int, quiz_question_update_data: QuizQuestionUpdate, db: AsyncSession):
    try:
        quiz_question_to_update_result = await db.execute(select(QuizQuestion).where(and_(QuizQuestion.quiz_id == quiz_id, QuizQuestion.question_id == quiz_question_id)))
        quiz_question_to_update = quiz_question_to_update_result.scalars().one()
        if not quiz_question_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question not found")
        
        for key, value in quiz_question_update_data.model_dump(exclude_unset=True).items():
            setattr(quiz_question_to_update, key, value)

        db.add(quiz_question_to_update)
        await db.commit()
        db.refresh(quiz_question_to_update)
        return quiz_question_to_update
    except HTTPException as e:
        await db.rollback()
        logger.error(f"mute_quiz_question Error: {e}")
        raise e
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"mute_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz Question Already Exists")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"mute_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in updating Quiz Question")
    except Exception as e:
        await db.rollback()
        logger.error(f"mute_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in updating Quiz Question")

# Remove a Quiz Question
async def remove_quiz_question(quiz_id: int, quiz_question_id: int, db: AsyncSession):
    try:
        quiz_question_to_delete = await db.get(QuizQuestion, (quiz_id, quiz_question_id))
        if not quiz_question_to_delete:
            raise ValueError("Quiz Question not found")
        await db.delete(quiz_question_to_delete)
        await db.commit()
        return {"message": "Quiz Question deleted successfully!"}
    except ValueError as e:
        await db.rollback()
        logger.error(f"remove_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"remove_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in deleting Quiz Question")
    except Exception as e:
        await db.rollback()
        logger.error(f"remove_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in deleting Quiz Question")

