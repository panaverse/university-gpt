

from fastapi import APIRouter

from api.quiz.answersheet.models import AnswerSheet, AnswerSheetCreate,AnswerSheetRead


router = APIRouter()

@router.post("", response_model=AnswerSheetRead)
async def create_answer_sheet(answer_sheet: AnswerSheetCreate):
    return await AnswerSheet.create(answer_sheet)

@router.get("", response_model=list[AnswerSheetRead])
async def read_answer_sheets(offset: int = 0, limit: int = 10):
    return await AnswerSheet.read_all(offset, limit)

@router.get("/{answer_sheet_id}", response_model=AnswerSheetRead)
async def read_answer_sheet(answer_sheet_id: int):
    return await AnswerSheet.read_one(answer_sheet_id)

@router.patch("/{answer_sheet_id}", response_model=AnswerSheetRead)
async def update_answer_sheet(answer_sheet_id: int, answer_sheet: AnswerSheetCreate):
    return await AnswerSheet.update(answer_sheet_id, answer_sheet)

@router.delete("/{answer_sheet_id}")
async def delete_answer_sheet(answer_sheet_id: int):
    return await AnswerSheet.delete(answer_sheet_id)

