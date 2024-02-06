from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select, text

from api.core.database import get_session
from api.quiz.question.models import QuestionBank, MCQOption

# ------------------------------------------------------
# ----------------- Question CRUD -----------------
# ------------------------------------------------------

# Add Question to the Database
def add_question(question: QuestionBank, session: Session):
    """
    Add a question to the database.

    Args:
        question (QuestionBank): The question object to be added.
        session (Session): The database session.

    Returns:
        QuestionBank: The added question.

    """

    db_question = QuestionBank.model_validate(question)
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question

# Get all Questions
def read_questions(offset: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    """
    Get all questions from the database.

    Args:
        offset (int): The offset value for pagination.
        limit (int): The limit value for pagination.
        db (Session): The database session.

    Returns:
        List[QuestionBank]: The list of questions.

    """

    questions = db.exec(select(QuestionBank).offset(offset).limit(limit)).all()
    return questions

# Get all Questions For a Question Type
def read_questions_by_type(question_type: str, db: Session = Depends(get_session)):
    """
    Get all questions of a specific question type from the database.

    Args:
        question_type (str): The name of the question type.
        db (Session): The database session.

    Returns:
        List[QuestionBank]: The list of questions.

    """

    questions = db.exec(select(QuestionBank).where(QuestionBank.question_type == question_type)).all()
    return questions

# Get a Question by ID
def get_question_by_id(id: int, db: Session = Depends(get_session)):
    """
    Get a question by its ID from the database.

    Args:
        id (int): The ID of the question.
        db (Session): The database session.

    Returns:
        QuestionBank: The retrieved question.

    """

    question = db.get(QuestionBank, id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question

# Update a Question by ID
def update_question(id: int, question: QuestionBank, db: Session = Depends(get_session)):
    """
    Update a question by its ID in the database.

    Args:
        id (int): The ID of the question to be updated.
        question (QuestionBank): The updated question object.
        db (Session): The database session.

    Returns:
        QuestionBank: The updated question.

    """

    question_to_update = db.get(QuestionBank, id)
    if not question_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    question_data = question.model_dump(exclude_unset=True)
    for key, value in question_data.items():
        setattr(question_to_update, key, value)
    db.add(question_to_update)
    db.commit()
    db.refresh(question_to_update)
    return question_to_update

# Delete a Question by ID
def delete_question(id: int, db: Session = Depends(get_session)):
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
    question = db.get(QuestionBank, id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}


# ------------------------------------------------------
# ----------------- MCQ Options CRUD -----------------
# ------------------------------------------------------

# Add MCQ Option to the Database
def add_mcq_option(mcq_option: MCQOption, session: Session):
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
    session.commit()
    session.refresh(db_mcq_option)
    return db_mcq_option

# Get all MCQ Options
def read_mcq_options(offset: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    mcq_options = db.exec(select(MCQOption).offset(offset).limit(limit)).all()
    return mcq_options

# Get a MCQ Option by ID
def get_mcq_option_by_id(id: int, db: Session = Depends(get_session)):
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
    mcq_option = db.get(MCQOption, id)
    if not mcq_option:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCQ Option not found")
    return mcq_option

# Update a MCQ Option by ID
def update_mcq_option(id: int, mcq_option: MCQOption, db: Session = Depends(get_session)):
    """
    Update an MCQ option by its ID.

    Args:
        id (int): The ID of the MCQ option to update.
        mcq_option (MCQOption): The updated MCQ option.
        db (Session, optional): The database session. Defaults to Depends(get_session).

    Returns:
        MCQOption: The updated MCQ option.

    Raises:
        HTTPException: If the MCQ option with the given ID is not found.
    """
    mcq_option_to_update = db.get(MCQOption, id)
    if not mcq_option_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCQ Option not found")
    mcq_option_data = mcq_option.model_dump(exclude_unset=True)
    for key, value in mcq_option_data.items():
        setattr(mcq_option_to_update, key, value)
    db.add(mcq_option_to_update)
    db.commit()
    db.refresh(mcq_option_to_update)
    return mcq_option_to_update

# Delete a MCQ Option by ID
def delete_mcq_option(id: int, db: Session = Depends(get_session)):
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
    mcq_option = db.get(MCQOption, id)
    if not mcq_option:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCQ Option not found")
    db.delete(mcq_option)
    db.commit()
    return {"message": "MCQ Option deleted successfully"}