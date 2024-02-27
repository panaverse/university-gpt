from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.database import get_session
from app.core.utils.logger import logger_config
from app.quiz.question.models import QuestionBankCreate
from app.quiz.quiz.models import (QuizCreate, QuizUpdate, QuizReadWithTopics, QuizUpdate,
                                  QuizReadWithQuestionsAndTopics, QuizQuestionReadQuestionBank, QuizQuestionRead, RuntimeQuizGenerated,
                                  QuizSettingCreate, QuizSettingRead, QuizSettingUpdate
                                  )
from app.quiz.quiz.crud import (quiz_engine, quiz_question_engine, quiz_setting_engine)


router = APIRouter(prefix="/quiz-engine")

logger = logger_config(__name__)


#-------------------------------------------
#             # QuizSetting Endpoints
#-------------------------------------------

router_quiz_setting = APIRouter()

# Create a new QuizSetting
@router_quiz_setting.post("", response_model=QuizSettingRead)
async def create_new_quiz_setting(quiz_setting: QuizSettingCreate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Create a new QuizSetting
    """
    try: 
        return await quiz_setting_engine.create_quiz_setting(db=db, quiz_setting=quiz_setting)
    except Exception as err:
        logger.error(f"create_new_quiz_setting Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating QuizSetting")

# Get all QuizSettings
@router_quiz_setting.get("", response_model=list[QuizSettingRead])
async def get_all_quiz_settings_endpoint(quiz_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Get all QuizSettings
    """
    try:
        return await quiz_setting_engine.get_all_quiz_settings_for_quiz(db=db, quiz_id=quiz_id)
    except Exception as err:
        logger.error(f"get_all_quiz_settings_endpoint Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching QuizSettings")

# Get a QuizSetting by ID
@router_quiz_setting.get("/{quiz_setting_id}", response_model=QuizSettingRead)
async def get_quiz_setting_by_id_endpoint(quiz_setting_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Get a QuizSetting by ID
    """
    try:
        return await quiz_setting_engine.get_quiz_setting_by_id(db=db, quiz_setting_id=quiz_setting_id)
    except Exception as err:
        logger.error(f"get_quiz_setting_by_id_endpoint Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QuizSetting not found")

# Update a QuizSetting
@router_quiz_setting.patch("/{quiz_setting_id}", response_model=QuizSettingRead)
async def update_quiz_setting_endpoint(quiz_setting_id: int, quiz_setting_update: QuizSettingUpdate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Update a QuizSetting
    """
    try:
        quiz_setting = await quiz_setting_engine.update_quiz_setting(db=db, quiz_setting_id=quiz_setting_id, quiz_setting_update=quiz_setting_update)
        if not quiz_setting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QuizSetting not found")
        return quiz_setting
    except Exception as err:
        logger.error(f"update_quiz_setting_endpoint Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in updating QuizSetting")


# ------------------------------
# Quiz Router Endpoints
# ------------------------------

quiz_router = APIRouter()

@quiz_router.post("", response_model=QuizReadWithQuestionsAndTopics)
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
        return await quiz_engine.create_quiz(quiz=quiz, db=db)

    except HTTPException as http_err:
        logger.error(f"create_new_quiz Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"create_new_quiz Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz")


@quiz_router.get("/all/{course_id}", response_model=list[QuizReadWithTopics])
async def call_read_all_quizzes(course_id: int, db: Annotated[AsyncSession, Depends(get_session)], offset: int = Query(default=0, lte=10), limit: int = Query(default=10, lte=100)):
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
        return await quiz_engine.read_all_quizzes_for_course(db=db, course_id=course_id, offset=offset, limit=limit)

    except HTTPException as http_err:
        logger.error(f"read_all_quizzes Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"read_all_quizzes Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quizzes")


@quiz_router.get("/{quiz_id}", response_model=QuizReadWithQuestionsAndTopics)
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

        quiz_called = await quiz_engine.read_quiz_by_id(quiz_id=quiz_id, db=db)
        return quiz_called

    except HTTPException as http_err:
        logger.error(f"read_quiz_by_id Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"read_quiz_by_id Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")


@quiz_router.patch("/{quiz_id}", response_model=QuizReadWithQuestionsAndTopics)
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
        return await quiz_engine.update_quiz(quiz_id=quiz_id, quiz_update_data=quiz, db=db)

    except HTTPException as http_err:
        logger.error(f"update_existing_quiz Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"update_existing_quiz Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")


@quiz_router.delete("/delete/{quiz_id}")
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
        quiz_del = await quiz_engine.delete_quiz(quiz_id=quiz_id, db=db)
        return quiz_del
    except HTTPException as http_err:
        logger.error(f"delete_existing_quiz Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"delete_existing_quiz Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

# ------------------------------
# Quiz Question Router Endpoints
# ------------------------------

quiz_question_router = APIRouter()

@quiz_question_router.post("/{quiz_id}/quiz-question", response_model=QuizQuestionReadQuestionBank)
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
        return await quiz_question_engine.create_quiz_question(quiz_id=quiz_id, quiz_question_create_data=quiz_question_data, db=db)

    except HTTPException as http_err:
        logger.error(f"create_new_quiz_question Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"create_new_quiz_question Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Error in creating Quiz Question")


@quiz_question_router.delete("/{quiz_id}/quiz-question/{quiz_question_id}")
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

    logger.info(f"Removing existing Quiz Question: {__name__}")

    try:
        return await quiz_question_engine.remove_quiz_question(quiz_id=quiz_id, quiz_question_id=quiz_question_id, db=db)
    except HTTPException as http_err:
        logger.error(f"remove_quiz_question Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"remove_quiz_question Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Quiz Question not found")


router.include_router(router_quiz_setting, tags=["QuizSetting"], prefix="/quiz-setting")
router.include_router(quiz_router, tags=["Quiz"], prefix="/quiz")
router.include_router(quiz_question_router, tags=["QuizQuestion"], prefix="/quiz")