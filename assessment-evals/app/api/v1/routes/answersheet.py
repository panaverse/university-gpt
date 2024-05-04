from fastapi import APIRouter, HTTPException, BackgroundTasks, status, Depends
from typing import Annotated, Optional, List
from app.api.deps import DBSessionDep, GetCurrentStudentDep, oauth2_scheme

from app.core.config import logger_config
from app.core.requests import validate_quiz_key
from app.service.quiz_attempt_manager import create_new_quiz_attempt, handle_in_progress_quiz_attempt
from app.crud.answersheet_crud import crud_answer_sheet, crud_answer_slot

from app.models.answersheet_model import AnswerSheetRead, AttemptQuizRequest
from app.models.answerslot_model import AnswerSlotCreate, AnswerSlotRead
from app.models.quiz_runtime_model import RuntimeQuizGenerated

logger = logger_config(__name__)

router = APIRouter()

# ------------------------------
# Get all Quiz Attempts for Student
# ------------------------------

@router.get("/all", response_model=list[AnswerSheetRead])
def get_all_quiz_attempts_for_student(
    db: DBSessionDep, student_data: GetCurrentStudentDep
):
    """
    Get All Quiz Attempts for Student
    """
    try:
        student_id = student_data["id"]
        quiz_attempts = crud_answer_sheet.all_quiz_attempts_for_student(
            db_session=db, student_id=student_id
        )
        return quiz_attempts

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unexpected Error Occured When Fetching Quiz Attempts"
        )


# ------------------------------
# Quiz Generation Endpoint
# ------------------------------

@router.post("/attempt", response_model=RuntimeQuizGenerated)
def generate_runtime_quiz_for_student(
    attempt_ids: AttemptQuizRequest, 
    db: DBSessionDep, 
    student_data: GetCurrentStudentDep
):
    """
    Take Quiz ID and Generate Quiz For Student
    Generate New Quiz Attempt for Student Or
    Returns In Progress Remaining Quiz Questions

    """
    logger.info(f"Generating Quiz for Student ID: {student_data['id']}")
    quiz_id = attempt_ids.quiz_id
    quiz_key = attempt_ids.quiz_key

    try:

        # # Check if quiz key is valid
        quiz_key_validated = validate_quiz_key(
            quiz_id=quiz_id, quiz_key=quiz_key
        )

        attempt_sheet = crud_answer_sheet.student_answer_sheet_exists(
            db, user_id=student_data["id"], quiz_id=quiz_id, quiz_key=quiz_key
        )

        if not attempt_sheet:
            return create_new_quiz_attempt(db=db, student_id=student_data['id'], quiz_id=quiz_id, quiz_key=quiz_key, quiz_key_validated=quiz_key_validated)

        return handle_in_progress_quiz_attempt(db=db,  attempt_sheet=attempt_sheet, student_id=student_data["id"], quiz_key_validated=quiz_key_validated)
            
    except HTTPException as http_err:
        logger.error(f"generate_quiz Error: {http_err}")
        raise http_err
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as err:
        logger.error(f"generate_quiz Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unexpected Error Occured When Generating Quiz"
        )


# ~ Get Quiz Attempt By ID
@router.get("/{quiz_attempt_id}", response_model=AnswerSheetRead)
def get_quiz_attempt_by_id(
    quiz_attempt_id: int, db: DBSessionDep, student_data: GetCurrentStudentDep
):
    """
    Gets a Quiz Answer Sheet by its id
    """
    try:
        student_id = student_data["id"]
        answer_sheet_obj = crud_answer_sheet.get_answer_sheet_by_id(
            db_session=db, answer_sheet_id=quiz_attempt_id, student_id=student_id
        )
        if not answer_sheet_obj:
            raise HTTPException(status_code=404, detail="Quiz Attempt Not Found")
        return answer_sheet_obj

    except HTTPException as http_err:
        raise http_err
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ~ Update Quiz Attempt - Finish Quiz


@router.patch("/{answer_sheet_id}/finish")
def update_quiz_attempt(answer_sheet_id: int, db_session: DBSessionDep, student_data: GetCurrentStudentDep):
    """
    Update Quiz Attempt
    """
    try:
        quiz_attempt_response = crud_answer_sheet.finish_answer_sheet_attempt(
            db_session=db_session, answer_sheet_id=answer_sheet_id, student_id=student_data["id"]
        )
        return quiz_attempt_response

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# # ---------------------
# # QuizAnswerSlot
# # ---------------------


@router.post("/answer_slot/save", response_model=AnswerSlotRead)
def save_quiz_answer_slot(
    background_tasks: BackgroundTasks,
    quiz_answer_slot: AnswerSlotCreate,
    db_session: DBSessionDep,
    student_data: GetCurrentStudentDep
):
    """
    Saves a student attempted Quiz Answer Slot
    """
    try:
        student_id=student_data["id"]
        # 1. ValidateIf Quiz is Active & Quiz Attempt ID is Valid
        quiz_attempt = crud_answer_sheet.is_answer_sheet_active(
            db_session=db_session,
            answer_sheet_id=quiz_answer_slot.quiz_answer_sheet_id,
            student_id=student_id,
        )

        print("\n\n\n quiz_attempt", quiz_attempt, "\n\n\n")
        if not quiz_attempt:
            raise ValueError("Quiz Time has Ended or Invalid Quiz Attempt ID")

        # 2. Save Quiz Answer Slot
        quiz_answer_slot_response = crud_answer_slot.create_quiz_answer_slot(
            db_session, quiz_answer_slot
        )

        # 2.1 RUN A BACKGROUND TASK TO UPDATE THE POINTS AWARDED
        background_tasks.add_task(
            crud_answer_slot.grade_quiz_answer_slot,
            db_session=db_session,
            quiz_answer_slot=quiz_answer_slot_response,
        )

        # 3. Return Quiz Answer Slot
        return quiz_answer_slot_response

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# # ---------------------
# # QuizFeedback - All Questions + Answers
# # ---------------------

@router.get("/{answer_sheet_id}/view-all-answers")
def get_quiz_feedback(
    answer_sheet_id: int, db_session: DBSessionDep, student_data: GetCurrentStudentDep
):
    """
    Get Quiz Feedback
    """
    try:
        student_id = student_data["id"]
        quiz_feedback = crud_answer_sheet.get_quiz_feedback(
            db_session=db_session, answer_sheet_id=answer_sheet_id, student_id=student_id
        )
        
        overview = quiz_feedback
        quiz_answers = quiz_feedback.quiz_answers
        
        return {"overview": overview, "quiz_answers_attempted": quiz_answers}
        

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


