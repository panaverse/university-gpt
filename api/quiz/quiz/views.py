from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from api.core.database import get_session
from api.quiz.quiz.crud import (create_quiz, read_all_quizzes, read_quiz_by_id, update_quiz, delete_quiz, 
                                create_quiz_topic, read_quiz_topics_for_quiz, read_quiz_topic, update_quiz_topic, delete_quiz_topic,
                                create_quiz_question_instance, read_quiz_question_instances_for_quiz, read_quiz_question_instance, update_quiz_question_instance, delete_quiz_question_instance
                                )
from api.quiz.quiz.models import QuizCreate, QuizRead, QuizUpdate, QuizReadWithQuizTopics, QuizTopicRead, QuizTopicCreate, QuizTopicUpdate, QuizTopicsReadWithTopic, QuizTopicRead, QuizQuestionInstancesCreate, QuizQuestionInstancesRead, QuizQuestionInstancesUpdate
from api.core.utils.logger import logger_config

router = APIRouter()    

logger = logger_config(__name__)

# ------------------------------
# Quiz Router Endpoints
# ------------------------------

@router.post("", response_model=QuizReadWithQuizTopics)
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
    
@router.get("", response_model=list[QuizRead])
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

@router.get("/{quiz_id}", response_model=QuizReadWithQuizTopics)
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
    
@router.patch("/{quiz_id}", response_model=QuizReadWithQuizTopics)
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
# Quiz Topic Router Endpoints
# ------------------------------

@router.post("/quiz-topic", response_model=QuizTopicRead)
async def create_new_quiz_topic(quiz_topic: QuizTopicCreate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Create a new Quiz Topic

    Args:
        quiz_topic (QuizTopicCreate): Quiz Topic to be created

    Returns:
        QuizTopicRead: The created Quiz Topic

    Raises:
        HTTPException: Error in creating Quiz Topic
    """

    logger.info(f"Creating new Quiz Topic: {__name__}, {quiz_topic}")

    try:
        return await create_quiz_topic(quiz_topic=quiz_topic, db=db)
    
    except HTTPException as http_err:
        logger.error(f"create_new_quiz_topic Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"create_new_quiz_topic Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz Topic")
    
@router.get("/{quiz_id}/quiz-topic", response_model=list[QuizTopicRead])
async def get_all_quiz_topics_for_quiz(quiz_id: int, db: Annotated[AsyncSession, Depends(get_session)], offset: int = Query(default=0, lte=10), limit: int = Query(default=10, lte=100)):
    """
    Read all Quiz Topics

    Args:
        offset (int, optional): Offset for pagination. Defaults to 0.
        limit (int, optional): Limit for pagination. Defaults to 10.

    Returns:
        list[QuizTopicRead]: List of Quiz Topics

    Raises:
        HTTPException: Error in fetching Quiz Topics
    """

    logger.info(f"Reading all Quiz Topics: {__name__}")

    try:
        return await read_quiz_topics_for_quiz(quiz_id=quiz_id, db=db, offset=offset, limit=limit)
    
    except HTTPException as http_err:
        logger.error(f"read_all_quiz_topics Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"read_all_quiz_topics Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quiz Topics")
    
@router.get("/quiz-topic/{quiz_topic_id}", response_model=QuizTopicsReadWithTopic)
async def read_quiz_topic_by_id(quiz_topic_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Read a Quiz Topic by ID

    Args:
        quiz_topic_id (int): ID of the Quiz Topic

    Returns:
        QuizTopicRead: The Quiz Topic

    Raises:
        HTTPException: Quiz Topic not found
    """

    logger.info(f"Reading Quiz Topic by ID: {__name__}, {quiz_topic_id}")

    try:
        return await read_quiz_topic(quiz_topic_id, db)
    
    except HTTPException as http_err:
        logger.error(f"read_quiz_topic_by_id Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"read_quiz_topic_by_id Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Topic not found")

@router.patch("/quiz-topic/{quiz_topic_id}", response_model=QuizTopicRead)
async def update_existing_quiz_topic(quiz_topic_id: int, quiz_topic: QuizTopicUpdate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Partially Update an existing Quiz Topic

    Args:
        quiz_topic_id (int): ID of the Quiz Topic
        quiz_topic (QuizTopicUpdate): Updated Quiz Topic Data

    Returns:
        QuizTopicRead: The updated Quiz Topic

    Raises:
        HTTPException: Quiz Topic not found
    """

    logger.info(f"Updating existing Quiz Topic: { __name__}, quiz_topic_id:{quiz_topic_id}, quiz_topic: {quiz_topic}")

    try:
        return await update_quiz_topic(quiz_topic_id, quiz_topic, db)
    
    except HTTPException as http_err:
        logger.error(f"update_existing_quiz_topic Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"update_existing_quiz_topic Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Topic not found")
    
@router.delete("/quiz-topic/{quiz_topic_id}")
async def delete_existing_quiz_topic(quiz_topic_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Delete an existing Quiz Topic

    Args:
        quiz_topic_id (int): ID of the Quiz Topic

    Returns:
        dict: Success Message

    Raises:
        HTTPException: Quiz Topic not found
    """

    logger.info(f"Deleting existing Quiz Topic:, {__name__} {quiz_topic_id}")

    try:
        return await delete_quiz_topic(quiz_topic_id, db)
    except HTTPException as http_err:
        logger.error(f"delete_existing_quiz_topic Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"delete_existing_quiz_topic Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Topic not found")

# ------------------------------
# Quiz Question Instances Router Endpoints
# ------------------------------
    
@router.post("/quiz-question-instance", response_model=QuizQuestionInstancesRead)
async def create_new_quiz_question_instance(quiz_question_instance: QuizQuestionInstancesCreate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Create a new Quiz Question Instance

    Args:
        quiz_question_instance (QuizQuestionInstanceCreate): Quiz Question Instance to be created

    Returns:
        QuizQuestionInstanceRead: The created Quiz Question Instance

    Raises:
        HTTPException: Error in creating Quiz Question Instance
    """

    logger.info(f"Creating new Quiz Question Instance: {__name__}, {quiz_question_instance}")

    try:
        return await create_quiz_question_instance(quiz_question_instance=quiz_question_instance, db=db)
    
    except HTTPException as http_err:
        logger.error(f"create_new_quiz_question_instance Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"create_new_quiz_question_instance Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz Question Instance")
    
@router.get("/{quiz_id}/quiz-question-instance", response_model=list[QuizQuestionInstancesRead])
async def get_all_quiz_question_instances_for_quiz(quiz_id: int, db: Annotated[AsyncSession, Depends(get_session)], offset: int = Query(default=0, lte=50), limit: int = Query(default=50, lte=200)):
    """
    Read all Quiz Question Instances

    Args:
        offset (int, optional): Offset for pagination. Defaults to 0.
        limit (int, optional): Limit for pagination. Defaults to 10.

    Returns:
        list[QuizQuestionInstanceRead]: List of Quiz Question Instances

    Raises:
        HTTPException: Error in fetching Quiz Question Instances
    """

    logger.info(f"Reading all Quiz Question Instances: {__name__}")

    try:
        return await read_quiz_question_instances_for_quiz(quiz_id=quiz_id, db=db, offset=offset, limit=limit)
    
    except HTTPException as http_err:
        logger.error(f"read_all_quiz_question_instances Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"read_all_quiz_question_instances Error: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quiz Question Instances")
    
@router.get("/quiz-question-instance/{quiz_question_instance_id}", response_model=QuizQuestionInstancesRead)
async def read_quiz_question_instance_by_id(quiz_question_instance_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Read a Quiz Question Instance by ID

    Args:
        quiz_question_instance_id (int): ID of the Quiz Question Instance

    Returns:
        QuizQuestionInstanceRead: The Quiz Question Instance

    Raises:
        HTTPException: Quiz Question Instance not found
    """

    logger.info(f"Reading Quiz Question Instance by ID: {__name__}, {quiz_question_instance_id}")

    try:
        return await read_quiz_question_instance(quiz_question_instance_id, db)
    
    except HTTPException as http_err:
        logger.error(f"read_quiz_question_instance_by_id Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"read_quiz_question_instance_by_id Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question Instance not found")               
    
@router.patch("/quiz-question-instance/{quiz_question_instance_id}", response_model=QuizQuestionInstancesRead)
async def update_existing_quiz_question_instance(quiz_question_instance_id: int, quiz_question_instance: QuizQuestionInstancesUpdate, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Partially Update an existing Quiz Question Instance

    Args:
        quiz_question_instance_id (int): ID of the Quiz Question Instance
        quiz_question_instance (QuizQuestionInstanceUpdate): Updated Quiz Question Instance Data

    Returns:
        QuizQuestionInstanceRead: The updated Quiz Question Instance

    Raises:
        HTTPException: Quiz Question Instance not found
    """

    logger.info(f"Updating existing Quiz Question Instance: { __name__}, quiz_question_instance_id:{quiz_question_instance_id}, quiz_question_instance: {quiz_question_instance}")

    try:
        return await update_quiz_question_instance(quiz_question_instance_id, quiz_question_instance, db)
    
    except HTTPException as http_err:
        logger.error(f"update_existing_quiz_question_instance Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"update_existing_quiz_question_instance Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question Instance not found")
    
@router.delete("/quiz-question-instance/{quiz_question_instance_id}")
async def delete_existing_quiz_question_instance(quiz_question_instance_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Delete an existing Quiz Question Instance

    Args:
        quiz_question_instance_id (int): ID of the Quiz Question Instance

    Returns:
        dict: Success Message

    Raises:
        HTTPException: Quiz Question Instance not found
    """

    logger.info(f"Deleting existing Quiz Question Instance:, {__name__} {quiz_question_instance_id}")

    try:
        return await delete_quiz_question_instance(quiz_question_instance_id, db)
    except HTTPException as http_err:
        logger.error(f"delete_existing_quiz_question_instance Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"delete_existing_quiz_question_instance Error: {err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question Instance not found")