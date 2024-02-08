from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.core.database import get_session
from api.quiz.qiuz.models import QuizRead,Quiz,QuizTopic, QuizTopicRead

router = APIRouter()    

@router.post("", response_model=QuizRead)
async def create_quiz(quiz_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalars().first()
    return quiz

@router.post("/quiz-topic", response_model=QuizTopicRead)
async def create_quiz_topic(quiz_topic_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(QuizTopic).where(QuizTopic.id == quiz_topic_id))
    quiz_topic = result.scalars().first()
    return quiz_topic

@router.get("", response_model=list[QuizRead])
async def read_quizzes(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Quiz).offset(offset).limit(limit))
    quizzes = result.scalars().all()
    return quizzes

@router.get("/quiz-topic", response_model=list[QuizTopicRead])
async def read_quiz_topics(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(QuizTopic).offset(offset).limit(limit))
    quiz_topics = result.scalars().all()
    return quiz_topics

@router.get("/{quiz_id}", response_model=QuizRead)
async def read_quiz(quiz_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalars().first()
    return quiz

@router.get("/quiz-topic/{quiz_topic_id}", response_model=QuizTopicRead)
async def read_quiz_topic(quiz_topic_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(QuizTopic).where(QuizTopic.id == quiz_topic_id))
    quiz_topic = result.scalars().first()
    return quiz_topic

@router.patch("/{quiz_id}", response_model=QuizRead)
async def update_quiz(quiz_id: int, quiz: QuizRead, db: AsyncSession = Depends(get_session)):
    quiz_to_update = await read_quiz(quiz_id, db)
    for key, value in quiz.model_dump().items() :
        setattr(quiz_to_update, key, value)
    await db.commit()
    db.refresh(quiz_to_update)
    return quiz_to_update

@router.patch("/quiz-topic/{quiz_topic_id}", response_model=QuizTopicRead)
async def update_quiz_topic(quiz_topic_id: int, quiz_topic: QuizTopicRead, db: AsyncSession = Depends(get_session)):
    quiz_topic_to_update = await read_quiz_topic(quiz_topic_id, db)
    for key, value in quiz_topic.model_dump().items() :
        setattr(quiz_topic_to_update, key, value)
    await db.commit()
    db.refresh(quiz_topic_to_update)
    return quiz_topic_to_update

@router.delete("/{quiz_id}")
async def delete_quiz(quiz_id: int, db: AsyncSession = Depends(get_session)):
    quiz_to_delete = await read_quiz(quiz_id, db)
    db.delete(quiz_to_delete)
    await db.commit()
    return {"message": "Quiz deleted successfully!"}

@router.delete("/quiz-topic/{quiz_topic_id}")
async def delete_quiz_topic(quiz_topic_id: int, db: AsyncSession = Depends(get_session)):
    quiz_topic_to_delete = await read_quiz_topic(quiz_topic_id, db)
    db.delete(quiz_topic_to_delete)
    await db.commit()
    return {"message": "Quiz Topic deleted successfully!"}
