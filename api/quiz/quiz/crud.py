from fastapi import HTTPException, status

from sqlmodel import select, and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.core.utils.logger import logger_config
from api.quiz.quiz.models import (Quiz, QuizCreate, QuizUpdate,
                                  QuizTopic, QuizTopicCreate, QuizTopicUpdate,
                                QuizQuestionInstances, QuizQuestionInstancesCreate, QuizQuestionInstancesUpdate

                                  )
from api.quiz.topic.models import Topic
from api.quiz.question.models import QuestionBank

logger = logger_config(__name__)

# Create Quiz
async def create_quiz(quiz: QuizCreate, db: AsyncSession):
    try:

        if quiz.quiz_topics:
            quiz.quiz_topics = [QuizTopic.model_validate(quiz_topic) for quiz_topic in quiz.quiz_topics]

        quiz_to_db = Quiz.model_validate(quiz)

        db.add(quiz_to_db)
        await db.commit()
        db.refresh(quiz_to_db)

        return quiz_to_db

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
        result = await db.execute(select(Quiz).offset(offset).limit(limit))
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
            select(Quiz).options(selectinload(Quiz.quiz_topics)).where(Quiz.id == quiz_id)
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

async def update_quiz(quiz_id: int, quiz: QuizUpdate, db: AsyncSession):

    try:
        quiz_to_update = await read_quiz_by_id(quiz_id, db)

        if quiz.quiz_topics:
            quiz.quiz_topics = [QuizTopic.model_validate(each_quiz_topic) for each_quiz_topic in quiz.quiz_topics]
            # Append new topics to existing topics
            # quiz_to_update.quiz_topics.extend(quiz.quiz_topics)
            # This replaces the existing quiz_topics with the new list
            quiz_to_update.quiz_topics.clear()  # Clear the existing items
            quiz_to_update.quiz_topics.extend(quiz.quiz_topics)  # Add new items





        for key, value in quiz.model_dump(exclude_unset=True, exclude={'quiz_topics'}).items():
            setattr(quiz_to_update, key, value)

        logger.info(f"AFTER Updating Quiz: {quiz_to_update}")
        logger.info(f"AFTER Updating Quiz: {quiz_to_update.quiz_topics}")

        db.add(quiz_to_update)
        await db.commit()
        db.refresh(quiz_to_update)
        return quiz_to_update

    except IntegrityError as e:
        await db.rollback()
        logger.error(f"update_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz Already Exists")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"update_quiz Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in updating Quiz")
    except Exception as e:
        await db.rollback()
        logger.error(f"update_quiz Error: {e}")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
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
# Quiz Topics
# -----------------------------

async def create_quiz_topic(quiz_topic: QuizTopicCreate, db: AsyncSession):
    try:
        quiz_topic_to_db = QuizTopic.model_validate(quiz_topic)
        
        db.add(quiz_topic_to_db)
        await db.commit()
        db.refresh(quiz_topic_to_db)
        
        return quiz_topic_to_db
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"create_quiz_topic Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz Topic Already Exists")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"create_quiz_topic Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in creating Quiz Topic")
    except Exception as e:
        await db.rollback()
        logger.error(f"create_quiz_topic Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in creating Quiz Topic")

async def read_quiz_topics_for_quiz(quiz_id:int, offset: int, limit: int, db: AsyncSession):
    try:
        result = await db.execute(select(QuizTopic).where(QuizTopic.quiz_id == quiz_id).offset(offset).limit(limit))
        quiz_topics = result.scalars().all()
        if not quiz_topics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Topics not found")
        return quiz_topics
    except HTTPException as e:
        await db.rollback()
        logger.error(f"read_all_quiz_topics Error: {e}")
        raise e
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"read_all_quiz_topics Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in fetching Quiz Topics")
    except Exception as e:
        await db.rollback()
        logger.error(f"read_all_quiz_topics Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in fetching Quiz Topics")

async def read_quiz_topic(quiz_topic_id: int, db: AsyncSession):
    try:
        # quiz_topic = await db.get(QuizTopic, quiz_topic_id)
        result = await db.execute(
            select(QuizTopic).options(selectinload(QuizTopic.topic).selectinload(Topic.questions).selectinload(QuestionBank.options)).where(QuizTopic.id == quiz_topic_id)
            )
        quiz_topic = result.scalars().one()
        if not quiz_topic:
            raise ValueError("Quiz Topic not found")
        
        logger.info(f"FETCHED QUIZ TOPIC: {quiz_topic.topic.questions[0].options}")
        if quiz_topic.topic:
            questions_info = [str(question) for question in quiz_topic.topic.questions]  # Adjust according to how you want to represent a question
            logger.info(f"FETCHED QUIZ TOPIC QUESTIONS: {questions_info}")
        else:
            logger.info(f"Quiz topic with ID {quiz_topic_id} has no associated topic.")

        return quiz_topic
    except ValueError as e:
        await db.rollback()
        logger.error(f"read_quiz_topic Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Topic not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"read_quiz_topic Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in fetching Quiz Topic")
    except Exception as e:
        await db.rollback()
        logger.error(f"read_quiz_topic Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in fetching Quiz Topic")

async def update_quiz_topic(quiz_topic_id: int, quiz_topic: QuizTopicUpdate, db: AsyncSession):
    try:
        quiz_topic_to_update = await read_quiz_topic(quiz_topic_id, db)
        for key, value in quiz_topic.model_dump(exclude_unset=True).items():
            setattr(quiz_topic_to_update, key, value)
        db.add(quiz_topic_to_update)
        await db.commit()
        db.refresh(quiz_topic_to_update)
        return quiz_topic_to_update
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"update_quiz_topic Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz Topic Already Exists")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"update_quiz_topic Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in updating Quiz Topic")
    except Exception as e:
        await db.rollback()
        logger.error(f"update_quiz_topic Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in updating Quiz Topic")

async def delete_quiz_topic(quiz_topic_id: int, db: AsyncSession):
    try:
        quiz_topic_to_delete = await db.get(QuizTopic, quiz_topic_id)
        if not quiz_topic_to_delete:
            raise ValueError("Quiz Topic not found")
        await db.delete(quiz_topic_to_delete)
        await db.commit()
        return {"message": "Quiz Topic deleted successfully!"}
    except ValueError as e:
        await db.rollback()
        logger.error(f"delete_quiz_topic Error: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Quiz Topic not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"delete_quiz_topic Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in deleting Quiz Topic")
    except Exception as e:
        await db.rollback()
        logger.error(f"delete_quiz_topic Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in deleting Quiz Topic")

# -----------------------------
# Quiz Question Instances
# -----------------------------
    
async def create_quiz_question_instance(quiz_question_instance: QuizQuestionInstancesCreate, db: AsyncSession):
    try:
        quiz_question_instance_to_db = QuizQuestionInstances.model_validate(quiz_question_instance)
        db.add(quiz_question_instance_to_db)
        await db.commit()
        db.refresh(quiz_question_instance_to_db)
        return quiz_question_instance_to_db
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"create_quiz_question_instance Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz Question Instance Already Exists")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"create_quiz_question_instance Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in creating Quiz Question Instance")
    except Exception as e:
        await db.rollback()
        logger.error(f"create_quiz_question_instance Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in creating Quiz Question Instance")
    
async def read_quiz_question_instances_for_quiz(quiz_id:int, offset: int, limit: int, db: AsyncSession):
    try:
        result = await db.execute(select(QuizQuestionInstances).where(QuizQuestionInstances.quiz_id == quiz_id).offset(offset).limit(limit))
        quiz_question_instances = result.scalars().all()
        if not quiz_question_instances:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question Instances not found")
        return quiz_question_instances
    except HTTPException as e:
        await db.rollback()
        logger.error(f"read_all_quiz_question_instances Error: {e}")
        raise e
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"read_all_quiz_question_instances Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in fetching Quiz Question Instances")
    except Exception as e:
        await db.rollback()
        logger.error(f"read_all_quiz_question_instances Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in fetching Quiz Question Instances")
    
async def read_quiz_question_instance(quiz_question_instance_id: int, db: AsyncSession):
    try:
        quiz_question_instance = await db.get(QuizQuestionInstances, quiz_question_instance_id)
        if not quiz_question_instance:
            raise ValueError("Quiz Question Instance not found")
        return quiz_question_instance
    except ValueError as e:
        await db.rollback()
        logger.error(f"read_quiz_question_instance Error: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Quiz Question Instance not found")
    
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"read_quiz_question_instance Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in fetching Quiz Question Instance")
    
    except Exception as e:
        await db.rollback()
        logger.error(f"read_quiz_question_instance Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in fetching Quiz Question Instance")
    
async def update_quiz_question_instance(quiz_question_instance_id: int, quiz_question_instance: QuizQuestionInstancesUpdate, db: AsyncSession):
    try:
        quiz_question_instance_to_update = await read_quiz_question_instance(quiz_question_instance_id, db)
        for key, value in quiz_question_instance.model_dump(exclude_unset=True).items():
            setattr(quiz_question_instance_to_update, key, value)
        db.add(quiz_question_instance_to_update)
        await db.commit()
        db.refresh(quiz_question_instance_to_update)
        return quiz_question_instance_to_update
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"update_quiz_question_instance Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz Question Instance Already Exists")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"update_quiz_question_instance Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in updating Quiz Question Instance")
    except Exception as e:
        await db.rollback()
        logger.error(f"update_quiz_question_instance Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in updating Quiz Question Instance")
    
async def delete_quiz_question_instance(quiz_question_instance_id: int, db: AsyncSession):
    try:
        quiz_question_instance_to_delete = await db.get(QuizQuestionInstances, quiz_question_instance_id)
        if not quiz_question_instance_to_delete:
            raise ValueError("Quiz Question Instance not found")
        await db.delete(quiz_question_instance_to_delete)
        await db.commit()
        return {"message": "Quiz Question Instance deleted successfully!"}
    except ValueError as e:
        await db.rollback()
        logger.error(f"delete_quiz_question_instance Error: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Quiz Question Instance not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"delete_quiz_question_instance Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in deleting Quiz Question Instance")
    except Exception as e:
        await db.rollback()
        logger.error(f"delete_quiz_question_instance Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in deleting Quiz Question Instance")
    
