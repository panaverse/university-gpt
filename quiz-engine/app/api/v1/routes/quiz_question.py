from fastapi import APIRouter, Query, HTTPException, status

from app.api.deps import DBSessionDep
from app.core.config import logger_config
from app.models.question_models import QuestionBankCreate
from app.models.quiz_models import (
    QuizQuestionReadQuestionBank,
)
from app.crud.quiz_question_crud import quiz_question_engine


logger = logger_config(__name__)


router = APIRouter()


@router.post(
    "/{quiz_id}/quiz-question", response_model=QuizQuestionReadQuestionBank
)
def create_new_quiz_question(
    quiz_id: int, quiz_question_data: QuestionBankCreate, db: DBSessionDep
):
    """
    Create a new Quiz Question

    Args:
        quiz_id (int): ID of the Quiz
        quiz_question_data (QuestionBankCreate): Quiz Question Data to add in QuestionBank and Link to QuizQuestion

    Returns:
        QuizQuestion: The created Quiz Question

    Raises:
        HTTPException: Error in creating Quiz Question
    """

    logger.info(f"Creating new Quiz Question: {__name__}, {quiz_question_data}")

    try:
        return quiz_question_engine.create_quiz_question(
            quiz_id=quiz_id, quiz_question_create_data=quiz_question_data, db=db
        )

    except HTTPException as http_err:
        logger.error(f"create_new_quiz_question Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"create_new_quiz_question Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error in creating Quiz Question",
        )


@router.delete("/{quiz_id}/quiz-question/{quiz_question_id}")
def call_remove_quiz_question(
    quiz_id: int, quiz_question_id: int, db: DBSessionDep
):
    """
    Remove an existing Quiz Question

    Args:
        quiz_question_id (int): ID of the Quiz Question

    Returns:
        dict: Success Message

    Raises:
        HTTPException: Quiz Question not found
    """

    logger.info(f"Removing existing Quiz Question: {__name__}")

    try:
        return quiz_question_engine.remove_quiz_question(
            quiz_id=quiz_id, quiz_question_id=quiz_question_id, db=db
        )
    except HTTPException as http_err:
        logger.error(f"remove_quiz_question Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"remove_quiz_question Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question not found"
        )


