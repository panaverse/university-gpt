from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from api.core.database import get_session
from api.core.utils.logger import logger_config
from api.quiz.question.models import  QuestionBankCreate
from api.quiz.quiz.models import ( QuizCreate, QuizUpdate, QuizReadWithTopics, QuizUpdate,  QuizQuestionUpdate, QuizReadWithQuestionsAndTopics, QuizQuestionReadQuestionBank, QuizQuestionRead)
from api.quiz.quiz.crud import(create_quiz, read_all_quizzes, delete_quiz, read_quiz_by_id, update_quiz,
                               create_quiz_question, mute_quiz_question, remove_quiz_question
                               )

router = APIRouter()    

logger = logger_config(__name__)

# ------------------------------
# Quiz Router Endpoints
# ------------------------------

@router.post("", response_model=QuizReadWithTopics)
async def create_new_quiz(quiz: QuizCreate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Create a new Quiz

    Args:
        quiz (QuizCreate): Quiz to be created

    Returns:
        QuizReadWithQuizTopics: The created Quiz and QuizTopics Included

    Raises:
        HTTPException: Error in creating Quiz
    """

    logger.info(f"Creating new Quiz:, {__name__}, {quiz}")

    try:
        return await create_quiz(quiz=quiz, db=db)
    
    except HTTPException as http_err:
        logger.error(f"create_new_quiz Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"create_new_quiz Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz")

@router.get("", response_model=list[QuizReadWithTopics])
async def call_read_all_quizzes(db: Annotated[AsyncSession, Depends(get_session)], offset: int = Query(default=0, lte=10), limit: int = Query(default=10, lte=100)):
    """
    Read all Quizzes

    Args:
        offset (int, optional): Offset for pagination. Defaults to 0.
        limit (int, optional): Limit for pagination. Defaults to 10.

    Returns:
        list[QuizReadWithTopics]: List of Quizzes with QuizTopics Included

    Raises:
        HTTPException: Error in fetching Quizzes
    """

    logger.info(f"Reading all Quizzes: {__name__}")

    try:
        return await read_all_quizzes(db=db, offset=offset, limit=limit)
    
    except HTTPException as http_err:
        logger.error(f"read_all_quizzes Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"read_all_quizzes Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quizzes")

@router.get("/{quiz_id}", response_model=QuizReadWithQuestionsAndTopics)
async def call_read_quiz_by_id(quiz_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Read a Quiz by ID

    Args:
        quiz_id (int): ID of the Quiz

    Returns:
        QuizReadWithQuizTopics: The Quiz with QuizTopics Included

    Raises:
        HTTPException: Quiz not found
    """

    logger.info(f"Reading Quiz by ID: {__name__}, {quiz_id}")

    try:
    
        quiz_called= await read_quiz_by_id(quiz_id=quiz_id, db=db)
        return quiz_called
    
    except HTTPException as http_err:
        logger.error(f"read_quiz_by_id Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"read_quiz_by_id Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    
@router.patch("/{quiz_id}", response_model=QuizReadWithQuestionsAndTopics)
async def update_existing_quiz(quiz_id: int, quiz: QuizUpdate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Partially Update an existing Quiz

    Args:
        quiz_id (int): ID of the Quiz
        quiz (QuizUpdate): Updated Quiz Data

    Returns:
        QuizReadWithQuizTopics: The updated Quiz with QuizTopics Included

    Raises:
        HTTPException: Quiz not found
    """

    logger.info(f"Updating existing Quiz:, {__name__}, quiz_id: {quiz_id}, quiz: {quiz}")

    try:
        return await update_quiz(quiz_id, quiz, db)
    
    except HTTPException as http_err:
        logger.error(f"update_existing_quiz Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"update_existing_quiz Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    
@router.delete("/{quiz_id}")
async def delete_existing_quiz(quiz_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Delete an existing Quiz

    Args:
        quiz_id (int): ID of the Quiz

    Returns:
        dict: Success Message

    Raises:
        HTTPException: Quiz not found
    """

    logger.info(f"Deleting existing Quiz: {__name__}, quiz_id: {quiz_id}")

    try:
        return await delete_quiz(quiz_id=quiz_id, db=db)
    except HTTPException as http_err:
        logger.error(f"delete_existing_quiz Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"delete_existing_quiz Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

# ------------------------------
# Quiz Question Router Endpoints
# ------------------------------
    
@router.post("/{quiz_id}/quiz-question", response_model=QuizQuestionReadQuestionBank)
async def create_new_quiz_question(quiz_id: int, quiz_question_data: QuestionBankCreate, db: Annotated[AsyncSession, Depends(get_session)]):
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
        return await create_quiz_question(quiz_id=quiz_id, quiz_question_create_data=quiz_question_data, db=db)
    
    except HTTPException as http_err:
        logger.error(f"create_new_quiz_question Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"create_new_quiz_question Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz Question")

@router.patch("{quiz_id}/quiz-question/{quiz_question_id}", response_model=QuizQuestionRead)
async def call_mute_quiz_question(quiz_id: int, quiz_question_id: int, quiz_mute_data: QuizQuestionUpdate,  db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Mute an existing Quiz Question

    Args:
        quiz_question_id (int): ID of the Quiz Question

    Returns:
        dict: Success Message

    Raises:
        HTTPException: Quiz Question not found
    """

    logger.info(f"Muting existing Quiz Question: {__name__}, quiz_question_id: {quiz_question_id}")

    try:
        return await mute_quiz_question(quiz_id=quiz_id, quiz_question_id=quiz_question_id, quiz_question_update_data=quiz_mute_data, db=db)
    except HTTPException as http_err:
        logger.error(f"mute_quiz_question Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"mute_quiz_question Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question not found")

@router.delete("{quiz_id}/quiz-question/{quiz_question_id}")
async def call_remove_quiz_question(quiz_id: int, quiz_question_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Remove an existing Quiz Question

    Args:
        quiz_question_id (int): ID of the Quiz Question

    Returns:
        dict: Success Message

    Raises:
        HTTPException: Quiz Question not found
    """

    logger.info(f"Removing existing Quiz Question: {__name__}, quiz_question_id: {quiz_question_id}")

    try:
        return await remove_quiz_question(quiz_id=quiz_id, quiz_question_id=quiz_question_id, db=db)
    except HTTPException as http_err:
        logger.error(f"remove_quiz_question Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"remove_quiz_question Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question not found")
