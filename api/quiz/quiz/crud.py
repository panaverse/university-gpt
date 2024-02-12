from fastapi import HTTPException, status

from sqlmodel import select, and_, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.core.utils.logger import logger_config
from api.quiz.topic.models import Topic
from api.quiz.question.models import QuestionBank, QuestionBankCreate, MCQOption
from api.quiz.user.models import Student
from api.quiz.quiz.models import (Quiz, QuizCreate, QuizUpdate,
                                  QuizUpdate, QuizQuestion, QuizQuestionUpdate)
from datetime import datetime
import random

logger = logger_config(__name__)

# Create Quiz
async def create_quiz(quiz: QuizCreate, db: AsyncSession):
    try:
        question_ids = set()  # Use a set to avoid duplicate question IDs

        # Validate Any New Topics
        if quiz.topics:
            quiz.topics = [Topic.model_validate(new_topic) for new_topic in quiz.topics]

        # Get all topics if topic_ids are provided and append to quiz.topics
        if quiz.topic_ids:
            topics_and_subtopics = await db.execute(select(Topic).options(selectinload(Topic.children_topics)).where(Topic.id.in_(quiz.topic_ids)))
            topics_from_db = topics_and_subtopics.scalars().all()
            if not topics_from_db:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Topic IDs Provided")
            quiz.topics.extend(topics_from_db)

            # Merge fetched topics with validated topics, ensuring uniqueness
            all_topics = {topic.id: topic for topic in quiz.topics}.values()

            # Collect all unique topic and subtopic IDs
            all_topic_ids = {topic.id for topic in all_topics}
            all_topic_ids.update({child.id for topic in all_topics for child in topic.children_topics})

            # Fetch all unique questions linked to these topics and subtopics
            questions_result = await db.execute(select(QuestionBank.id).where(QuestionBank.topic_id.in_(all_topic_ids), QuestionBank.is_verified == True))
            question_ids.update(questions_result.scalars().all())

        quiz_to_db = Quiz.model_validate(quiz)

        db.add(quiz_to_db)
        await db.commit()
        db.refresh(quiz_to_db)

        if question_ids:
            quiz_questions_instances = [QuizQuestion(quiz_id=quiz_to_db.id, question_id=question_id) for question_id in question_ids]
            db.add_all(quiz_questions_instances)

        await db.commit()

        db.refresh(quiz_to_db)

        # Fetch the quiz with the topics and questions
        quiz_added = await read_quiz_by_id(quiz_to_db.id, db)

        # Update quiz points - based on the sum of all question points
        quiz_added.total_points = sum([quiz_question.question.points for quiz_question in quiz_added.quiz_questions])
        await db.commit()
        db.refresh(quiz_added)

        return quiz_added

    except HTTPException as http_err:
        await db.rollback()
        logger.error(f"create_quiz Error: {http_err}")
        raise http_err

    except Exception as e:
        await db.rollback()
        logger.error(f"create_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


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

        # Initialize a set to track IDs of newly added topics and subtopics
        newly_added_topic_ids = set()

        # Determine new and existing topic IDs for optimized querying
        existing_topic_ids = {topic.id for topic in quiz_to_update.topics}
        new_topic_ids = set(quiz_update_data.add_topic_ids) - \
            existing_topic_ids if quiz_update_data.add_topic_ids else set()
        topics_to_remove = set(quiz_update_data.remove_topic_ids) if quiz_update_data.remove_topic_ids else set()

        # Add new topics and their subtopics if not already associated
        new_topics_with_subtopics = []
        if new_topic_ids:
            new_topics_with_subtopics = await db.execute(
                select(Topic).options(selectinload(Topic.children_topics))
                .where(Topic.id.in_(new_topic_ids))
            )
            for topic in new_topics_with_subtopics.scalars():
                if topic.id not in existing_topic_ids:
                    quiz_to_update.topics.append(topic)
                    # Ensure the topic ID is marked as added
                    newly_added_topic_ids.add(topic.id)
                for child in topic.children_topics:
                    if child.id not in existing_topic_ids and child.id not in new_topic_ids:
                        quiz_to_update.topics.append(child)
                        # Ensure the subtopic ID is marked as added
                        newly_added_topic_ids.add(child.id)

            await db.commit()

        # Query for questions related to new topics and subtopics
        if newly_added_topic_ids:
            questions_result = await db.execute(
                select(QuestionBank)
                .where(QuestionBank.topic_id.in_(list(newly_added_topic_ids)), QuestionBank.is_verified == True)
            )
            questions_to_add = questions_result.scalars().all()

            new_quiz_questions = [QuizQuestion(
                quiz_id=quiz_id, question_id=question.id) for question in questions_to_add]

            db.add_all(new_quiz_questions)
            await db.commit()

        # Update Quiz Data Fields
        for key, value in quiz_update_data.model_dump(exclude_unset=True).items():
            if hasattr(quiz_to_update, key):
                setattr(quiz_to_update, key, value)

        # Remove specified topics and their questions
        if topics_to_remove:
            # Efficiently remove topics and their subtopics if specified
            quiz_to_update.topics = [
                topic for topic in quiz_to_update.topics if topic.id not in topics_to_remove]
            # Remove questions linked to these topics
            await db.execute(
                delete(QuizQuestion)
                .where(QuizQuestion.question_id.in_(
                    select(QuestionBank.id).where(
                        QuestionBank.topic_id.in_(topics_to_remove))
                ), QuizQuestion.quiz_id == quiz_id)
            )

        await db.commit()

        # Expire all session data
        db.expire_all()

        # Re-fetch the quiz to ensure all changes are accurately reflected
        quiz_updated = await read_quiz_by_id(quiz_id, db)
        quiz_updated.total_points = sum(
            quiz_question_link.question.points for quiz_question_link in quiz_updated.quiz_questions)
        await db.commit()

        return quiz_updated

    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


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
        # 0. If quiz_question_create_data.is_verified is False Raise Error
        if not quiz_question_create_data.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Question must be verified as True to be added in Quiz")
        # 1. Get the quiz to link the question to
        quiz = await db.get(Quiz, quiz_id)
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

        # 2. Add Question to the QuestionBank then link to the Quiz using QuizQuestion Model
        if quiz_question_create_data.options:
            quiz_question_create_data.options = [MCQOption.model_validate(
                option) for option in quiz_question_create_data.options]

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Quiz Question Already Exists")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"create_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in creating Quiz Question")
    except Exception as e:
        await db.rollback()
        logger.error(f"create_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in creating Quiz Question")

# UPDATE Quiz Question


async def update_quiz_question(quiz_id: int, quiz_question_id: int, quiz_question_update_data: QuizQuestionUpdate, db: AsyncSession):
    try:
        quiz_question_to_update_result = await db.execute(select(QuizQuestion).where(and_(QuizQuestion.quiz_id == quiz_id, QuizQuestion.question_id == quiz_question_id)))
        quiz_question_to_update = quiz_question_to_update_result.scalars().one()
        if not quiz_question_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question not found")

        for key, value in quiz_question_update_data.model_dump(exclude_unset=True).items():
            setattr(quiz_question_to_update, key, value)

        db.add(quiz_question_to_update)
        await db.commit()
        db.refresh(quiz_question_to_update)
        return quiz_question_to_update
    except HTTPException as e:
        await db.rollback()
        logger.error(f"update_quiz_question Error: {e}")
        raise e
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"update_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Quiz Question Already Exists")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"update_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in updating Quiz Question")
    except Exception as e:
        await db.rollback()
        logger.error(f"update_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in updating Quiz Question")

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Quiz Question not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"remove_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in deleting Quiz Question")
    except Exception as e:
        await db.rollback()
        logger.error(f"remove_quiz_question Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in deleting Quiz Question")

# ------------------------------
# Quiz Generation Endpoint
# ------------------------------
    
# Take Quiz ID and Generate Quiz For Student
# 1. Verify Student ID & Quiz ID are valid & Quiz is between Start & End Date
# 2. Generate Quiz with Randomly Shuffled Questions    
# 3. Return Quiz with Questions
    
async def generate_quiz(quiz_id: int, student_id: int, db: AsyncSession):
    try:
        # 1. Verify Student ID
        student = await db.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        
        # 2. Verify Quiz ID
        quiz_with_question_result = await db.execute(select(Quiz).options(selectinload(Quiz.quiz_questions).joinedload(QuizQuestion.question).joinedload(QuestionBank.options)).where(Quiz.id == quiz_id))
        quiz_with_questions = quiz_with_question_result.scalars().one()
        if not quiz_with_questions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
        
        # 3. Verify Quiz is between Start & End Date
        if quiz_with_questions.start_date and quiz_with_questions.end_date:
            if not (quiz_with_questions.start_date <= datetime.now() <= quiz_with_questions.end_date):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz is not active")
        
        # 4. Generate Quiz with Randomly Shuffled Questions
        random.shuffle(quiz_with_questions.quiz_questions)

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