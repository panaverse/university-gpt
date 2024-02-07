from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import Depends
from api.core.database import get_session
from api.quiz.qiuz.models import Quiz, QuizCreate, QuizTopic, QuizTopicCreate


async def create_quiz(quiz: QuizCreate, db: AsyncSession = Depends(get_session)):
    quiz_to_db = Quiz.model_validate(quiz)
    db.add(quiz_to_db)
    await db.commit()
    db.refresh(quiz_to_db)
    return quiz_to_db

async def create_quiz_topic(quiz_topic: QuizTopicCreate, db: AsyncSession = Depends(get_session)):
    quiz_topic_to_db = QuizTopic.model_validate(quiz_topic)
    db.add(quiz_topic_to_db)
    await db.commit()
    db.refresh(quiz_topic_to_db)
    return quiz_topic_to_db

async def read_quizzes(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Quiz).offset(offset).limit(limit))
    quizzes = result.scalars().all()
    return quizzes

async def read_quiz(quiz_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalars().first()
    return quiz

async def update_quiz(quiz_id: int, quiz: QuizCreate, db: AsyncSession = Depends(get_session)):
    quiz_to_update = await read_quiz(quiz_id, db)
    for key, value in quiz.model_dump().items() :
        setattr(quiz_to_update, key, value)
    await db.commit()
    db.refresh(quiz_to_update)
    return quiz_to_update

async def delete_quiz(quiz_id: int, db: AsyncSession = Depends(get_session)):
    quiz_to_delete = await read_quiz(quiz_id, db)
    db.delete(quiz_to_delete)
    await db.commit()
    return {"message": "Quiz deleted successfully!"}