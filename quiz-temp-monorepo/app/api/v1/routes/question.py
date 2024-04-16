from fastapi import APIRouter, Query, HTTPException

from app.api.deps import AsyncSessionDep
from app.core.config import logger_config

from app.crud.question_crud import question_crud, mcq_crud
from app.models.question_models import (
    QuestionBankCreate,
    QuestionBankUpdate,
    QuestionBankRead,
    MCQOptionCreate,
    MCQOptionUpdate,
    MCQOptionRead,
)


router = APIRouter()

logger = logger_config(__name__)

# ------------------------------------------------------
# ----------------- Question CRUD View -----------------
# ------------------------------------------------------


@router.post("", response_model=QuestionBankRead)
async def create_new_question(question: QuestionBankCreate, db: AsyncSessionDep):
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
        return await question_crud.add_question(question=question, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=list[QuestionBankRead])
async def call_read_questions(
    db: AsyncSessionDep,
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
        all_questions = await question_crud.read_questions(
            db=db, offset=offset, limit=limit
        )
        return all_questions
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/read/{question_type}", response_model=list[QuestionBankRead])
async def call_read_questions_by_type(question_type: str, db: AsyncSessionDep):
    """
    Get all questions of a specific question type from the database.

    Args:
        question_type (str): The question type.
       db (optional) : Database Dependency Injection.

    Returns:
        list[QuestionBank]: The list of questions.
    """
    logger.info("%s.get_all_questions_by_type: %s", __name__, question_type)
    try:
        return await question_crud.read_questions_by_type(
            question_type=question_type, db=db
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{question_id}", response_model=QuestionBankRead)
async def call_get_question_by_id(question_id: int, db: AsyncSessionDep):
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
        return await question_crud.get_question_by_id(id=question_id, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{question_id}", response_model=QuestionBankRead)
async def call_update_question(
    question_id: int, question: QuestionBankUpdate, db: AsyncSessionDep
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
        return await question_crud.update_question(
            id=question_id, question=question, db=db
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{question_id}")
async def call_delete_question(question_id: int, db: AsyncSessionDep):
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
        return await question_crud.delete_question(id=question_id, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------
# ----------------- MCQ Question CRUD View -----------------
# ------------------------------------------------------


@router.get("/mcq-option/all", response_model=list[MCQOptionRead])
async def call_read_mcq_options(
    db: AsyncSessionDep,
    offset: int = Query(default=0, le=10),
    limit: int = Query(default=10, le=100),
):
    """
    Get all MCQ options from the database.

    Args:
       db (optional) : Database Dependency Injection.

    Returns:
        list[MCQOption]: The list of MCQ options.
    """
    logger.info("%s.get_all_mcq_options", __name__)
    try:
        return await mcq_crud.read_mcq_options(db=db, offset=offset, limit=limit)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mcq-option", response_model=MCQOptionRead)
async def call_add_mcq_option(mcq_option: MCQOptionCreate, db: AsyncSessionDep):
    """
    Add an MCQ option to the database.

    Args:
        mcq_option (MCQOption): The MCQ option to be added.
       db (optional) : Database Dependency Injection.

    Returns:
        MCQOption: The added MCQ option.
    """
    logger.info("%s.add_mcq_option: %s", __name__, mcq_option)
    try:
        return await mcq_crud.add_mcq_option(mcq_option=mcq_option, session=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mcq-option/{mcq_option_id}", response_model=MCQOptionRead)
async def call_get_mcq_option_by_id(mcq_option_id: int, db: AsyncSessionDep):
    """
    Get an MCQ option by its ID from the database.

    Args:
        mcq_option_id (int): The ID of the MCQ option.
       db (optional) : Database Dependency Injection.

    Returns:
        MCQOption: The retrieved MCQ option.
    """
    logger.info("%s.get_mcq_option_by_id: %s", __name__, mcq_option_id)
    try:
        return await mcq_crud.get_mcq_option_by_id(id=mcq_option_id, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/mcq-option/{mcq_option_id}", response_model=MCQOptionRead)
async def call_update_mcq_option(
    mcq_option_id: int, mcq_option: MCQOptionUpdate, db: AsyncSessionDep
):
    """
    Update an MCQ option by its ID in the database.

    Args:
        mcq_option_id (int): The ID of the MCQ option.
        mcq_option (MCQOption): The updated MCQ option.
       db (optional) : Database Dependency Injection.

    Returns:
        MCQOption: The updated MCQ option.
    """
    logger.info("%s.update_mcq_option: %s", __name__, mcq_option)
    try:
        return await mcq_crud.update_mcq_option(
            id=mcq_option_id, mcq_option=mcq_option, db=db
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/mcq-option/{mcq_option_id}")
async def call_delete_mcq_option(mcq_option_id: int, db: AsyncSessionDep):
    """
    Delete an MCQ option by its ID from the database.

    Args:
        mcq_option_id (int): The ID of the MCQ option.
       db (optional) : Database Dependency Injection.

    Returns:
        deletion status.
    """
    logger.info("%s.delete_mcq_option: %s", __name__, mcq_option_id)
    try:
        return await mcq_crud.delete_mcq_option(id=mcq_option_id, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
