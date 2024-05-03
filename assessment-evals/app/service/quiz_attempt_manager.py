from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.base import QuizAttemptStatus
from app.models.answersheet_model import AnswerSheetCreate
from app.core.requests import get_runtime_quiz_questions
from app.models.quiz_runtime_model import RuntimeQuizGenerated

from app.core.config import logger_config
from app.crud.answersheet_crud import crud_answer_sheet

logger = logger_config(__name__)


def create_new_quiz_attempt(*, db: Session, student_id: int, quiz_id: int, quiz_key: str, quiz_key_validated) -> RuntimeQuizGenerated:
    runtime_quiz = get_runtime_quiz_questions(quiz_id)
    answer_sheet = AnswerSheetCreate(
        student_id=student_id,
        quiz_id=quiz_id,
        quiz_key=quiz_key,
        time_limit=quiz_key_validated["time_limit"],
        total_points=runtime_quiz["total_points"],
        time_start=datetime.utcnow(),  # Use UTC time
        quiz_title=runtime_quiz["quiz_title"],
    )
    quiz_attempt_response = crud_answer_sheet.create_answer_sheet(db_session=db, answer_sheet_obj_in=answer_sheet)
    return build_response_object(quiz_attempt=quiz_attempt_response, 
                                 runtime_quiz=runtime_quiz, 
                                 instructions=quiz_key_validated["instructions"])


def handle_in_progress_quiz_attempt(*, db: Session, attempt_sheet, student_id: int, quiz_key_validated) -> RuntimeQuizGenerated:
    if attempt_sheet.status == QuizAttemptStatus.completed:
        print("Quiz Attempt Already Completed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already attempted this quiz.")
    elif attempt_sheet.status == QuizAttemptStatus.in_progress:
        # Additional check to ensure the quiz attempt is still active
        quiz_attempt = crud_answer_sheet.is_answer_sheet_active(
            db_session=db,
            answer_sheet_id=attempt_sheet.id,
            student_id=student_id,
        )
        if quiz_attempt is False:            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quiz Attempt Finished",
            )
        return resume_quiz_attempt(db=db, attempt_sheet=attempt_sheet, quiz_key_validated=quiz_key_validated)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid quiz attempt state.")


def resume_quiz_attempt(*, db: Session, attempt_sheet, quiz_key_validated):

    quiz_feedback = crud_answer_sheet.get_quiz_feedback(db, attempt_sheet.id, attempt_sheet.student_id)
    runtime_quiz = get_runtime_quiz_questions(attempt_sheet.quiz_id)
    remaining_questions = filter_answered_questions(runtime_quiz['quiz_questions'], quiz_feedback.quiz_answers)

    return build_response_object(quiz_attempt=attempt_sheet, 
                                 runtime_quiz=runtime_quiz, 
                                 remaining_questions=remaining_questions,
                                 instructions=quiz_key_validated["instructions"])


def filter_answered_questions(all_questions, answered_questions):
    answered_ids = {answer.question_id for answer in answered_questions}
    return [question for question in all_questions if question['id'] not in answered_ids]


def build_response_object(*, quiz_attempt, runtime_quiz, remaining_questions=None, instructions=None) -> RuntimeQuizGenerated:
    if remaining_questions is None:
        remaining_questions = runtime_quiz['quiz_questions']
        
    if instructions is None:
        instructions = "Attempt the quiz."

    return RuntimeQuizGenerated(
        answer_sheet_id=quiz_attempt.id,
        quiz_title=runtime_quiz['quiz_title'],
        course_id=runtime_quiz['course_id'],
        instructions=instructions,
        student_id=quiz_attempt.student_id,
        quiz_id=quiz_attempt.quiz_id,
        time_limit=quiz_attempt.time_limit,
        time_start=quiz_attempt.time_start,
        total_points=quiz_attempt.total_points,
        quiz_key=quiz_attempt.quiz_key,
        quiz_questions=remaining_questions,
    )
