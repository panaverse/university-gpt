from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.core.database import get_session
from app.quiz.answersheet.models import AnswerSheet, AnswerSheetCreate


async def create_answer_sheet(answer_sheet: AnswerSheetCreate, db: AsyncSession = Depends(get_session)):
    quiz_to_db = AnswerSheet.model_validate(answer_sheet)
    db.add(quiz_to_db)
    await db.commit()
    db.refresh(quiz_to_db)
    return quiz_to_db


async def read_answer_sheets(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(AnswerSheet).offset(offset).limit(limit))
    answer_sheets = result.scalars().all()
    return answer_sheets


async def read_answer_sheet(answer_sheet_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(AnswerSheet).where(AnswerSheet.id == answer_sheet_id))
    answer_sheet = result.scalars().first()
    return answer_sheet


async def update_answer_sheet(answer_sheet_id: int, answer_sheet: AnswerSheetCreate, db: AsyncSession = Depends(get_session)):
    answer_sheet_to_update = await read_answer_sheet(answer_sheet_id, db)
    for key, value in answer_sheet.model_dump().items():
        setattr(answer_sheet_to_update, key, value)
    await db.commit()
    db.refresh(answer_sheet_to_update)
    return answer_sheet_to_update


async def delete_answer_sheet(answer_sheet_id: int, db: AsyncSession = Depends(get_session)):
    answer_sheet_to_delete = await read_answer_sheet(answer_sheet_id, db)
    db.delete(answer_sheet_to_delete)
    await db.commit()
    return {"message": "Answer Sheet deleted successfully!"}
