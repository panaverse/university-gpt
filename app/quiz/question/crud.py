from fastapi import HTTPException, status
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSession
from app.quiz.question.models import QuestionBank, QuestionBankCreate, QuestionBankUpdate, MCQOption, MCQOptionCreate, MCQOptionUpdate
from app.core.utils.logger import logger_config

logger = logger_config(__name__)

# ------------------------------------------------------
# ----------------- Question CRUD -----------------
# ------------------------------------------------------

# Add Question to the Database


async def add_question(question: QuestionBankCreate, db: AsyncSession):
    """
    Add a question to the database.

    Args:
        question (QuestionBank): The question object to be added.
        db (AsyncSession): The database session.

    Returns:
        QuestionBank: The added question.

    """
    try:
        if question.options:
            question.options = [MCQOption.model_validate(
                option) for option in question.options]

        db_question = QuestionBank.model_validate(question)

        db.add(db_question)
        await db.commit()
        db.refresh(db_question)
        return db_question
    except IntegrityError as e:
        await db.rollback()  # Ensure rollback is awaited
        logger.error(
            f"ADD_Question: An integrity error occurred while adding the Question: {e}")
        raise HTTPException(status_code=500, detail="Data integrity issue.")

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(
            f"ADD_Question: A database error occurred while adding the Question: {e}")
        raise HTTPException(
            status_code=500, detail="Database operation failed.")

    except Exception as e:
        await db.rollback()
        logger.error(f"ADD_Question: An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred.")

# Get all Questions


async def read_questions(db: AsyncSession, offset: int, limit: int):
    """
    Get all questions from the database.

    Args:
        offset (int): The offset value for pagination.
        limit (int): The limit value for pagination.
        db (Session): The database session.

    Returns:
        List[QuestionBank]: The list of questions.

    """

    try:
        result = await db.execute(select(QuestionBank).offset(offset).limit(limit))
        questions = result.scalars().all()
        if not questions:
            raise ValueError("No questions found")
        return questions
    except ValueError as e:
        logger.error(f"READ_Questions: No questions found: {e}")
        await db.rollback()
        raise HTTPException(status_code=404, detail="No questions found")
    except SQLAlchemyError as e:
        logger.error(
            f"READ_Questions: A database error occurred while reading the Questions: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Database operation failed.")
    except Exception as e:
        logger.error(f"READ_Questions: An unexpected error occurred: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred.")

# Get all Questions For a Question Type


async def read_questions_by_type(question_type: str, db: AsyncSession):
    """
    Get all questions of a specific question type from the database.

    Args:
        question_type (str): The name of the question type.
        db (Session): The database session.

    Returns:
        List[QuestionBank]: The list of questions.

    """

    try:
        result = await db.execute(select(QuestionBank).where(QuestionBank.question_type == question_type))
        questions = result.scalars().all()

        if not questions:
            raise ValueError("questions not found")
        return questions

    except ValueError as e:
        await db.rollback()  # Ensure rollback is awaited
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No questions found") from e

    except SQLAlchemyError as e:
        await db.rollback()  # Ensure rollback is awaited
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database operation failed.") from e

    except Exception as e:
        await db.rollback()  # Ensure rollback is awaited
        raise Exception("An unexpected error occurred.") from e

# Get a Question by ID


async def get_question_by_id(id: int, db: AsyncSession):
    """
    Get a question by its ID from the database.

    Args:
        id (int): The ID of the question.
        db (Session): The database session.

    Returns:
        QuestionBank: The retrieved question.

    """

    try:
        # question = await db.get(QuestionBank, id)
        result = await db.execute(select(QuestionBank).where(QuestionBank.id == id))
        question = result.scalars().first()
        if not question:
            raise ValueError("Question not found")
        return question
    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database operation failed.") from e
    except Exception as e:
        await db.rollback()
        raise Exception("An unexpected error occurred.") from e

# Update a Question by ID
async def update_question(id: int, question: QuestionBankUpdate, db: AsyncSession):
    """
    Update a question by its ID in the database.

    Args:
        id (int): The ID of the question to be updated.
        question (QuestionBank): The updated question object.
        db (Session): The database session.

    Returns:
        QuestionBank: The updated question.

    """
    try:
        question_to_update = await db.get(QuestionBank, id)
        if not question_to_update:
            raise ValueError(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Question not found")
        question_data = question.model_dump(exclude_unset=True)
        for key, value in question_data.items():
            setattr(question_to_update, key, value)
        db.add(question_to_update)
        await db.commit()
        await db.refresh(question_to_update)
        return question_to_update
    except ValueError:
        await db.rollback()
        logger.error(f"UPDATE_Question: Question not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"UPDATE_Question: Error updating question: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database operation failed.") from e
    except Exception as e:
        await db.rollback()
        logger.error(f"UPDATE_Question: Error updating question: {str(e)}")
        raise Exception("Error updating question")

# Delete a Question by ID


async def delete_question(id: int, db: AsyncSession):
    """
    Deletes a question from the database.

    Args:
        id (int): The ID of the question to be deleted.
        db (Session, optional): The database session. Defaults to Depends(get_session).

    Raises:
        HTTPException: If the question with the given ID is not found.

    Returns:
        dict: A dictionary with a message indicating the successful deletion of the question.
    """
    try:
        question = await db.get(QuestionBank, id)
        if not question:
            raise ValueError("Question not found")
        await db.delete(question)
        await db.commit()
        return {"message": "Question deleted successfully"}
    except HTTPException as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database operation failed.") from e

# ------------------------------------------------------
# ----------------- MCQ Options CRUD -----------------
# ------------------------------------------------------

# Add MCQ Option to the Database


async def add_mcq_option(mcq_option: MCQOptionCreate, session: AsyncSession):
    """
    Retrieve all MCQ options from the database.

    Args:
        offset (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to retrieve. Defaults to 100.
        db (Session, optional): The database session. Defaults to Depends(get_session).

    Returns:
        List[MCQOption]: A list of MCQ options.
    """
    try:
        db_mcq_option = MCQOption.model_validate(mcq_option)
        session.add(db_mcq_option)
        await session.commit()
        await session.refresh(db_mcq_option)
        return db_mcq_option
    except IntegrityError as e:
        await session.rollback()
        logger.error(
            f"ADD_MCQ_Option: An integrity error occurred while adding the MCQ Option: {e}")
        raise HTTPException(status_code=500, detail="Data integrity issue.")
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(
            f"ADD_MCQ_Option: A database error occurred while adding the MCQ Option: {e}")
        raise HTTPException(
            status_code=500, detail="Database operation failed.")
    except Exception as e:
        await session.rollback()
        logger.error(f"ADD_MCQ_Option: An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred.")


# Get all MCQ Options
async def read_mcq_options(db: AsyncSession, offset: int, limit: int):
    try:
        result = await db.execute(select(MCQOption).offset(offset).limit(limit))
        mcq_options = result.scalars().all()
        if not mcq_options:
            raise ValueError("No MCQ options found")
        return mcq_options
    except ValueError as e:
        logger.error(f"READ_MCQ_Options: No MCQ options found: {e}")
        db.rollback()
        raise HTTPException(status_code=404, detail="No MCQ options found")
    except SQLAlchemyError as e:
        logger.error(
            f"READ_MCQ_Options: A database error occurred while reading the MCQ Options: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Database operation failed.")
    except Exception as e:
        logger.error(f"READ_MCQ_Options: An unexpected error occurred: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred.")

# Get a MCQ Option by ID


async def get_mcq_option_by_id(id: int, db: AsyncSession):
    """
    Retrieve an MCQ option by its ID.

    Args:
        id (int): The ID of the MCQ option to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_session).

    Returns:
        MCQOption: The retrieved MCQ option.

    Raises:
        HTTPException: If the MCQ option with the given ID is not found.
    """
    try:
        mcq_option = await db.get(MCQOption, id)
        if not mcq_option:
            raise ValueError("MCQ Option not found")
        return mcq_option
    except ValueError as e:
        await db.rollback()
        logger.error(f"GET_MCQ_Option: MCQ Option not found: {e}")
        raise HTTPException(status_code=404, detail="MCQ Option not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(
            f"GET_MCQ_Option: A database error occurred while retrieving the MCQ Option: {e}")
        raise HTTPException(
            status_code=500, detail="Database operation failed.")
    except Exception as e:
        await db.rollback()
        logger.error(f"GET_MCQ_Option: An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred.")


# Update a MCQ Option by ID
async def update_mcq_option(id: int, mcq_option: MCQOptionUpdate, db: AsyncSession):
    """
    Update an MCQ option by its ID.

    Args:
        id (int): The ID of the MCQ option to update.
        mcq_option (MCQOptionUpdate): The updated MCQ option.
        db (Session, optional): The database session. Defaults to Depends(get_session).

    Returns:
        MCQOption: The updated MCQ option.

    Raises:
        HTTPException: If the MCQ option with the given ID is not found.
    """
    try:
        mcq_option_to_update = await db.get(MCQOption, id)
        if not mcq_option_to_update:
            raise ValueError("MCQ Option not found")
        mcq_option_data = mcq_option.model_dump(exclude_unset=True)
        for key, value in mcq_option_data.items():
            setattr(mcq_option_to_update, key, value)
        db.add(mcq_option_to_update)
        await db.commit()
        await db.refresh(mcq_option_to_update)
        return mcq_option_to_update
    except ValueError as e:
        await db.rollback()
        logger.error(f"UPDATE_MCQ_Option: MCQ Option not found: {e}")
        raise HTTPException(status_code=404, detail="MCQ Option not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"UPDATE_MCQ_Option: Error updating MCQ Option: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Database operation failed.")
    except Exception as e:
        await db.rollback()
        logger.error(f"UPDATE_MCQ_Option: An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred.")

# Delete a MCQ Option by ID


async def delete_mcq_option(id: int, db: AsyncSession):
    """
    Delete an MCQ option by its ID.

    Args:
        id (int): The ID of the MCQ option to delete.
        db (Session, optional): The database session. Defaults to Depends(get_session).

    Returns:
        dict: A message indicating the success of the deletion.

    Raises:
        HTTPException: If the MCQ option with the given ID is not found.
    """
    try:
        mcq_option = await db.get(MCQOption, id)
        if not mcq_option:
            raise ValueError("MCQ Option not found")
        await db.delete(mcq_option)
        await db.commit()
        return {"message": "MCQ Option deleted successfully"}
    except ValueError as e:
        await db.rollback()
        logger.error(f"DELETE_MCQ_Option: MCQ Option not found: {e}")
        raise HTTPException(status_code=404, detail="MCQ Option not found")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"DELETE_MCQ_Option: Error deleting MCQ Option: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Database operation failed.")
    except Exception as e:
        await db.rollback()
        logger.error(f"DELETE_MCQ_Option: An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred.")
