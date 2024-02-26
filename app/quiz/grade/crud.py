from sqlmodel import text

from app.config import settings
from app.core.database import AsyncSession
from app.quiz.grade.models import Result, ResultCreate, ResultRead, ResultUpdate
from app.core.utils.logger import logger_config

logger = logger_config(__name__)


async def get_result(db: AsyncSession, result_id: int) -> Result:
    result = await db.get(Result, result_id)
    return result


async def get_results(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Result]:
    results = await db.execute(text(f"SELECT * FROM result LIMIT {limit} OFFSET {skip};"))
    return results.scalars().all()


async def create_result(db: AsyncSession, result: ResultCreate) -> Result:
    select_answer_sheet = text(
        f"SELECT * FROM answersheet WHERE id = {result.answer_sheet_id};")
    answer_sheet = await db.execute(select_answer_sheet)
    if not answer_sheet:
        raise ValueError("Answer sheet not found")
    # get answer and question ids from answer sheet
    answer_sheet = answer_sheet.scalars().first()
    answer_sheet = answer_sheet.answerJSON
    answer_sheet = answer_sheet.split(",")
    answer_sheet = [int(i) for i in answer_sheet]
    # get questions from quiz
    select_quiz = text(f"SELECT * FROM quiz WHERE id = {answer_sheet[0]};")
    quiz = await db.execute(select_quiz)
    if not quiz:
        raise ValueError("Quiz not found")
    quiz = quiz.scalars().first()
    quiz = quiz.questions
    quiz = quiz.split(",")
    quiz = [int(i) for i in quiz]
    # get correct answers from questions
    correct_answers = []
    for i in quiz:
        select_question = text(f"SELECT * FROM question WHERE id = {i};")
        question = await db.execute(select_question)
        if not question:
            raise ValueError("Question not found")
        question = question.scalars().first()
        correct_answers.append(question.correct_answer)
    # compare correct answers with answer sheet
    obtained_marks = 0
    for i in range(len(quiz)):
        if correct_answers[i] == answer_sheet[i+1]:
            obtained_marks += 1
    result.total_marks = len(quiz)
    result.obtained_marks = obtained_marks
    # create result
    db_result = Result(**result.dict())
    db.add(db_result)
    await db.commit()
    await db.refresh(db_result)
    return db_result


async def update_result(db: AsyncSession, result_id: int, result: ResultUpdate) -> Result:
    db_result = await db.get(Result, result_id)
    for key, value in result.dict().items():
        setattr(db_result, key, value) if value else None
    await db.commit()
    await db.refresh(db_result)
    return db_result


async def delete_result(db: AsyncSession, result_id: int) -> Result:
    db_result = await db.get(Result, result_id)
    db.delete(db_result)
    await db.commit()
    return db_result
