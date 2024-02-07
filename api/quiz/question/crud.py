from fastapi import HTTPException, status
from sqlmodel import select

from api.core.database import AsyncSession
from api.quiz.question.models import QuestionBank, QuestionBankCreate, QuestionBankUpdate ,MCQOption, MCQOptionCreate, MCQOptionUpdate

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
    if question.options:
        question.options = [MCQOption.model_validate(option) for option in question.options]

    db_question = QuestionBank.model_validate(question)

    db.add(db_question)
    await db.commit()
    db.refresh(db_question)
    return db_question

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

    result = await db.execute(select(QuestionBank).offset(offset).limit(limit))
    questions = result.scalars().all()
    return questions

# Get all Questions For a Question Type
async def read_questions_by_type(question_type: str, db: AsyncSession ):
    """
    Get all questions of a specific question type from the database.

    Args:
        question_type (str): The name of the question type.
        db (Session): The database session.

    Returns:
        List[QuestionBank]: The list of questions.

    """

    result = await db.execute(select(QuestionBank).where(QuestionBank.question_type == question_type))
    questions = result.scalars().all()
    return questions

# Get a Question by ID
async def get_question_by_id(id: int, db: AsyncSession ):
    """
    Get a question by its ID from the database.

    Args:
        id (int): The ID of the question.
        db (Session): The database session.

    Returns:
        QuestionBank: The retrieved question.

    """

    question = await db.get(QuestionBank, id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question

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

    question_to_update = await db.get(QuestionBank, id)
    if not question_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    question_data = question.model_dump(exclude_unset=True)
    for key, value in question_data.items():
        setattr(question_to_update, key, value)
    db.add(question_to_update)
    await db.commit()
    await db.refresh(question_to_update)
    return question_to_update

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
    question = await db.get(QuestionBank, id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    await db.delete(question)
    await db.commit()
    return {"message": "Question deleted successfully"}


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
    db_mcq_option = MCQOption.model_validate(mcq_option)
    session.add(db_mcq_option)
    await session.commit()
    await session.refresh(db_mcq_option)
    return db_mcq_option

# Get all MCQ Options
async def read_mcq_options(db: AsyncSession, offset: int, limit: int ):
    result = await db.execute(select(MCQOption).offset(offset).limit(limit))
    mcq_options = result.scalars().all()
    return mcq_options

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
    mcq_option = await db.get(MCQOption, id)
    if not mcq_option:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCQ Option not found")
    return mcq_option

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
    mcq_option_to_update = await db.get(MCQOption, id)
    if not mcq_option_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCQ Option not found")
    mcq_option_data = mcq_option.model_dump(exclude_unset=True)
    for key, value in mcq_option_data.items():
        setattr(mcq_option_to_update, key, value)
    db.add(mcq_option_to_update)
    await db.commit()
    await db.refresh(mcq_option_to_update)
    return mcq_option_to_update

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
    mcq_option = await db.get(MCQOption, id)
    if not mcq_option:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCQ Option not found")
    await db.delete(mcq_option)
    await db.commit()
    return {"message": "MCQ Option deleted successfully"}