from fastapi import APIRouter, Query, HTTPException

from app.api.deps import DBSessionDep
from app.core.config import logger_config

from app.crud.question_crud import question_crud
from app.models.question_models import (
    QuestionBankCreate,
    QuestionBankUpdate,
    QuestionBankRead,
)
from app.settings import GET_CUSTOM_GPT_SPEC


router = APIRouter()

logger = logger_config(__name__)

@router.post("", response_model=QuestionBankRead)
def create_new_question(question: QuestionBankCreate, db: DBSessionDep):
    """
    Add a question to the database.

    Args:
        question (QuestionBank): The question to be added.
        db (optional) : Database Dependency Injection.

    Returns:
        QuestionBank: The added question.
    """
    logger.info("%s.create_a_question: %s", __name__, question)
    try:
        return question_crud.add_question(question=question, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=list[QuestionBankRead])
def call_read_questions(
    db: DBSessionDep,
    offset: int = Query(default=0, le=10),
    limit: int = Query(default=10, le=100),
):
    """
    Get all questions from the database.

    Args:
        offset (int, optional): The offset for pagination. Defaults to 0.
        limit (int, optional): The limit for pagination. Defaults to 100.
       db (optional) : Database Dependency Injection.

    Returns:
        list[QuestionBank]: The list of questions.
    """
    logger.info("%s.get_all_questions", __name__)
    try:
        all_questions = question_crud.read_questions(
            db=db, offset=offset, limit=limit
        )
        return all_questions
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all questions by topic_id
@router.get("/read/topic/{topic_id}", response_model=list[QuestionBankRead])
def call_read_questions_by_topic(topic_id: int, db: DBSessionDep):
    """
    Get all questions of a specific topic from the database.

    Args:
        topic_id (int): The topic ID.
       db (optional) : Database Dependency Injection.

    Returns:
        list[QuestionBank]: The list of questions.
    """
    logger.info("%s.get_all_questions_by_topic: %s", __name__, topic_id)
    try:
        return question_crud.get_questions_by_topic(topic_id=topic_id, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/read/{question_type}", response_model=list[QuestionBankRead], include_in_schema=GET_CUSTOM_GPT_SPEC)
def call_read_questions_by_type(question_type: str, db: DBSessionDep):
    """
    Get all questions of a specific question type from the database.

    Args:
        question_type (str): The question type = "single_select_mcq" or "multiple_select_mcq"
       db (optional) : Database Dependency Injection.

    Returns:
        list[QuestionBank]: The list of questions.
    """
    logger.info("%s.get_all_questions_by_type: %s", __name__, question_type)
    try:
        return question_crud.read_questions_by_type(
            question_type=question_type, db=db
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@router.patch("/{question_id}", response_model=QuestionBankRead)
def call_update_question(
    question_id: int, question: QuestionBankUpdate, db: DBSessionDep
):
    """
    Update a question by its ID in the database.

    Args:
        question_id (int): The ID of the question.
        question (QuestionBank): The updated question.
        db (optional) : Database Dependency Injection.

    Returns:
        QuestionBank: The updated question.
    """
    logger.info("%s.update_question: %s", __name__, question)
    try:
        return question_crud.update_question(
            id=question_id, question=question, db=db
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{question_id}")
def call_delete_question(question_id: int, db: DBSessionDep):
    """
    Delete a question by its ID from the database.

    Args:
        question_id (int): The ID of the question.
       db (optional) : Database Dependency Injection.

    Returns:
        deletion status.
    """
    logger.info("%s.delete_question: %s", __name__, question_id)
    try:
        return question_crud.delete_question(id=question_id, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


