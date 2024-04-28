from fastapi import APIRouter, Query, HTTPException, status

from app.api.deps import DBSessionDep, CourseQuizDep
from app.core.config import logger_config
from app.models.quiz_models import (
    QuizCreate,
    QuizReadWithTopics,
    QuizUpdate,
    QuizReadWithQuestionsAndTopics,

)
from app.crud.quiz_crud import quiz_engine


router = APIRouter()

logger = logger_config(__name__)

@router.post("", response_model=QuizReadWithQuestionsAndTopics)
def create_new_quiz(quiz: QuizCreate, db: DBSessionDep, course: CourseQuizDep):
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
        gen_quiz = quiz_engine.create_quiz(quiz=quiz, db=db)
        return gen_quiz

    except HTTPException as http_err:
        logger.error(f"create_new_quiz Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"create_new_quiz Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz"
        )


@router.get("/all/{course_id}", response_model=list[QuizReadWithTopics])
def call_read_all_quizzes(
    course_id: int,
    db: DBSessionDep,
    offset: int = Query(default=0, lte=10),
    limit: int = Query(default=10, lte=100),
):
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
        return quiz_engine.read_all_quizzes_for_course(
            db=db, course_id=course_id, offset=offset, limit=limit
        )

    except HTTPException as http_err:
        logger.error(f"read_all_quizzes Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"read_all_quizzes Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quizzes"
        )


@router.get("/{quiz_id}", response_model=QuizReadWithQuestionsAndTopics)
def call_read_quiz_by_id(quiz_id: int, db: DBSessionDep):
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
        quiz_called = quiz_engine.read_quiz_by_id(quiz_id=quiz_id, db=db)
        return quiz_called

    except HTTPException as http_err:
        logger.error(f"read_quiz_by_id Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"read_quiz_by_id Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )


@router.patch("/{quiz_id}", response_model=QuizReadWithQuestionsAndTopics)
def update_existing_quiz(quiz_id: int, quiz: QuizUpdate, db: DBSessionDep):
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

    logger.info(
        f"Updating existing Quiz:, {__name__}, quiz_id: {quiz_id}, quiz: {quiz}"
    )

    try:
        return quiz_engine.update_quiz(
            quiz_id=quiz_id, quiz_update_data=quiz, db=db
        )

    except HTTPException as http_err:
        logger.error(f"update_existing_quiz Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"update_existing_quiz Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )


@router.delete("/delete/{quiz_id}")
def delete_existing_quiz(quiz_id: int, db: DBSessionDep):
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
        quiz_del = quiz_engine.delete_quiz(quiz_id=quiz_id, db=db)
        return quiz_del
    except HTTPException as http_err:
        logger.error(f"delete_existing_quiz Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"delete_existing_quiz Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )
