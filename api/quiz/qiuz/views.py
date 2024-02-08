from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.core.database import get_session
from api.quiz.qiuz.models import QuizRead,Quiz,QuizTopic, QuizTopicRead, QuizCreate, QuizTopicCreate
from api.quiz.qiuz.crud import create_quiz, create_quiz_topic, read_quizzes, read_quiz, update_quiz, delete_quiz

router = APIRouter()    

@router.post("", response_model=QuizRead)
async def call_create_quiz(quiz: QuizCreate, db: AsyncSession = Depends(get_session)):
    return await create_quiz(quiz=quiz, db=db)

@router.post("/quiz-topic", response_model=QuizTopicRead)
async def cal_create_quiz_topic(quiz_topic: QuizTopicCreate, db: AsyncSession = Depends(get_session)):
    return await create_quiz_topic(quiz_topic=quiz_topic, db=db)

@router.get("", response_model=list[QuizRead])
async def call_read_quizzes(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    return await read_quizzes(offset=offset, limit=limit, db=db)

@router.get("/quiz-topic", response_model=list[QuizTopicRead])
async def read_quiz_topics(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(QuizTopic).offset(offset).limit(limit))
    quiz_topics = result.scalars().all()
    return quiz_topics

@router.get("/{quiz_id}", response_model=QuizRead)
async def call_read_quiz(quiz_id: int, db: AsyncSession = Depends(get_session)):
    return await read_quiz(quiz_id, db)

@router.get("/quiz-topic/{quiz_topic_id}", response_model=QuizTopicRead)
async def read_quiz_topic(quiz_topic_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(QuizTopic).where(QuizTopic.id == quiz_topic_id))
    quiz_topic_in_db = result.scalars().first()
    return quiz_topic_in_db

@router.patch("/{quiz_id}", response_model=QuizRead)
async def call_update_quiz(quiz_id: int, quiz: QuizRead, db: AsyncSession = Depends(get_session)):
    return await update_quiz(quiz_id, quiz, db)

@router.patch("/quiz-topic/{quiz_topic_id}", response_model=QuizTopicRead)
async def update_quiz_topic(quiz_topic_id: int, quiz_topic: QuizTopicRead, db: AsyncSession = Depends(get_session)):
    quiz_topic_to_update = await read_quiz_topic(quiz_topic_id, db)
    for key, value in quiz_topic.model_dump(exclude_unset=True).items() :
        setattr(quiz_topic_to_update, key, value)
    await db.commit(quiz_topic_to_update)
    db.refresh(quiz_topic_to_update)
    return quiz_topic_to_update

@router.delete("/{quiz_id}")
async def call_delete_quiz(quiz_id: int, db: AsyncSession = Depends(get_session)):
    return await delete_quiz(quiz_id, db)

@router.delete("/quiz-topic/{quiz_topic_id}")
async def delete_quiz_topic(quiz_topic_id: int, db: AsyncSession = Depends(get_session)):
    quiz_topic_to_delete = await read_quiz_topic(quiz_topic_id, db)
    db.delete(quiz_topic_to_delete)
    await db.commit()
    return {"message": "Quiz Topic deleted successfully!"}
