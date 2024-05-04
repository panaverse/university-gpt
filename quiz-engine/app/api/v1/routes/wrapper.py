from fastapi import APIRouter, HTTPException, status

from app.api.deps import DBSessionDep
from app.core.config import logger_config

from app.crud.quiz_crud import runtime_quiz_engine
from app.crud.quiz_setting_crud import quiz_setting_engine
from app.models.quiz_runtime_model import WrapperRuntimeQuiz
from app.crud.question_crud import question_crud
from app.models.question_models import QuestionBankRead

logger = logger_config(__name__)

router = APIRouter()

# ------------------------------
# Runtime & Wrapper Endpoints
# ------------------------------


@router.get("/runtime-generation", response_model=WrapperRuntimeQuiz)
def generate_runtime_quiz_for_student(
   quiz_id:int, db: DBSessionDep
):
    logger.info(f"Generating Runtime Quiz: {__name__}")

    try:

        runtime_quiz = runtime_quiz_engine.generate_quiz(
            quiz_id=quiz_id, db=db
        )
        resp = WrapperRuntimeQuiz(
                total_points=runtime_quiz.total_points,
                quiz_title=runtime_quiz.quiz_title,
                course_id=runtime_quiz.course_id,
                quiz_questions=runtime_quiz.quiz_questions,
        )
        return resp
         
    except HTTPException as http_err:
        logger.error(f"generate_quiz Error: {http_err}")
        raise http_err
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as err:
        logger.error(f"generate_quiz Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

# Validate QUiz Key
@router.get("/validate-quiz-key")
def validate_quiz_key(
    quiz_id:int, quiz_key:str, db: DBSessionDep
):
    logger.info(f"Validating Quiz Key: {__name__}")

    try:

        quiz_key_validated = quiz_setting_engine.validate_quiz_key(
            db=db, quiz_id=quiz_id, quiz_key=quiz_key
        )
        return quiz_key_validated
         
    except HTTPException as http_err:
        logger.error(f"validate_quiz_key Error: {http_err}")
        raise http_err
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as err:
        logger.error(f"validate_quiz_key Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )
        
# Get a Question by ID

@router.get("/{question_id}", response_model=QuestionBankRead)
def call_get_question_by_id(question_id: int, db: DBSessionDep):
    """
    Get a question by its ID from the database.

    Args:
        question_id (int): The ID of the question.
       db (optional) : Database Dependency Injection.

    Returns:
        QuestionBank: The retrieved question.
    """
    logger.info("%s.get_question_by_id: %s", __name__, question_id)
    try:
        return question_crud.get_question_by_id(id=question_id, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))