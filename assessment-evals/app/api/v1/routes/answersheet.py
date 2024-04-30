from fastapi import APIRouter, HTTPException, BackgroundTasks, status
from datetime import datetime

from app.api.deps import DBSessionDep, GetCurrentStudentDep, LoginForAccessTokenDep
from app.core.config import logger_config

from app.crud.answersheet_crud import crud_answer_sheet, crud_answer_slot

from app.models.base import QuizAttemptStatus
from app.models.answersheet_model import (
    AnswerSheetCreate,
    AnswerSheetRead,
    AttemptQuizRequest,
)
from app.models.answerslot_model import AnswerSlotCreate, AnswerSlotRead
from app.models.quiz_runtime_model import RuntimeQuizGenerated
from app.core.requests import get_runtime_quiz_questions, validate_quiz_key



logger = logger_config(__name__)

router = APIRouter()

# ------------------------------
# Quiz Generation Endpoint
# ------------------------------


@router.post("/attempt", response_model=RuntimeQuizGenerated)
def generate_runtime_quiz_for_student(
    attempt_ids: AttemptQuizRequest, db: DBSessionDep, student_data: GetCurrentStudentDep
):
    """
    Take Quiz ID and Generate Quiz For Student
    Ensure student have not attempted the quiz before
    If QuizAttempt is Active,
        Generate Quiz with Randomly Shuffled Questions
        Return Quiz with Questions
    If QuizAttempt is Inactive,
        Return Error
    If Quiz Not Attempted Before,
        # 1. Verify Student ID & Quiz ID are valid & Quiz is between Start & End Date
        # 2. Generate Quiz with Randomly Shuffled Questions
        # 3. After calling it we will create Quiz Attempt and then return the Quiz with Questions

    """
    logger.info(f"Generating Quiz for Student: {__name__}")

    try:
        student_id = student_data["id"]

        # 0. Ensure student have not attempted the quiz before
        quiz_id: int = attempt_ids.quiz_id
        quiz_key: str = attempt_ids.quiz_key

        # Check if quiz key is valid
        quiz_key_validated = validate_quiz_key(
            quiz_id=quiz_id, quiz_key=quiz_key
        )

        attempt_sheet = crud_answer_sheet.student_answer_sheet_exists(
            db, user_id=student_id, quiz_id=quiz_id, quiz_key=quiz_key
        )
        if attempt_sheet is None:
            runtime_quiz = get_runtime_quiz_questions(
                quiz_id=quiz_id
            )

            # 1 Create Quiz Attempt
            answer_sheet_obj_in = AnswerSheetCreate(
                student_id=student_id,
                quiz_id=quiz_id,
                quiz_key=quiz_key,
                time_limit=quiz_key_validated["time_limit"],
                total_points=runtime_quiz["total_points"],
                time_start=datetime.now(),
            )

            quiz_attempt_response = crud_answer_sheet.create_answer_sheet(
                db_session=db, answer_sheet_obj_in=answer_sheet_obj_in
            )

            response_object = RuntimeQuizGenerated(
                answer_sheet_id=quiz_attempt_response.id,
                quiz_title=runtime_quiz["quiz_title"],
                course_id=runtime_quiz["course_id"],
                instructions=quiz_key_validated["instructions"],
                student_id=quiz_attempt_response.student_id,
                quiz_id=quiz_attempt_response.quiz_id,
                time_limit=quiz_attempt_response.time_limit,
                time_start=quiz_attempt_response.time_start,
                total_points=quiz_attempt_response.total_points,
                quiz_key=quiz_attempt_response.quiz_key,
                quiz_questions=runtime_quiz["quiz_questions"],
            )

            return response_object

        if attempt_sheet.status == QuizAttemptStatus.completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already attempted this quiz",
            )

        if attempt_sheet.status == QuizAttemptStatus.in_progress:
            # TODO: Return the quiz attempt in progress
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have an ongoing quiz attempt",
            )

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Quiz Attempt"
            )
            
            
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
