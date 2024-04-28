from fastapi import APIRouter, Query, HTTPException

from app.api.deps import DBSessionDep
from app.core.config import logger_config

from app.crud.answer_crud import mcq_crud
from app.models.answer_models import (
    MCQOptionCreate,
    MCQOptionRead,
    MCQOptionUpdate,
)


router = APIRouter()

logger = logger_config(__name__)

# Get all mcq options for a question_id
@router.get("/mcq-option/question/{question_id}", response_model=list[MCQOptionRead])
def call_get_mcq_options_by_question_id(
    question_id: int, db: DBSessionDep
):
    """
    Get all MCQ options by question_id from the database.

    Args:
        question_id (int): The ID of the question.
        db (optional) : Database Dependency Injection.

    Returns:
        list[MCQOption]: The list of MCQ options.
    """
    logger.info("%s.get_mcq_options_by_question_id: %s", __name__, question_id)
    try:
        return mcq_crud.get_mcq_options_by_question_id(
            question_id=question_id, db=db
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mcq-option/all", response_model=list[MCQOptionRead])
def call_read_mcq_options(
    db: DBSessionDep,
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
        return mcq_crud.read_mcq_options(db=db, offset=offset, limit=limit)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mcq-option", response_model=MCQOptionRead)
def call_add_mcq_option(mcq_option: MCQOptionCreate, db: DBSessionDep):
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
        return mcq_crud.add_mcq_option(mcq_option=mcq_option, session=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mcq-option/{mcq_option_id}", response_model=MCQOptionRead)
def call_get_mcq_option_by_id(mcq_option_id: int, db: DBSessionDep):
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
        return mcq_crud.get_mcq_option_by_id(id=mcq_option_id, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/mcq-option/{mcq_option_id}", response_model=MCQOptionRead)
def call_update_mcq_option(
    mcq_option_id: int, mcq_option: MCQOptionUpdate, db: DBSessionDep
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
        return mcq_crud.update_mcq_option(
            id=mcq_option_id, mcq_option=mcq_option, db=db
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/mcq-option/{mcq_option_id}")
def call_delete_mcq_option(mcq_option_id: int, db: DBSessionDep):
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
        return mcq_crud.delete_mcq_option(id=mcq_option_id, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
