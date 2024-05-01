from fastapi import APIRouter, HTTPException, status

from app.api.deps import DBSessionDep
from app.core.config import logger_config
from app.models.quiz_setting import (
    QuizSettingCreate,
    QuizSettingRead,
    QuizSettingUpdate,
)
from app.crud.quiz_setting_crud import quiz_setting_engine


router = APIRouter()

logger = logger_config(__name__)


router = APIRouter()


# Create a new QuizSetting
@router.post("", response_model=QuizSettingRead)
def create_new_quiz_setting(quiz_setting: QuizSettingCreate, db: DBSessionDep):
    """
    Create a new QuizSetting
    """
    try:
        return quiz_setting_engine.create_quiz_setting(
            db=db, quiz_setting=quiz_setting
        )
    except HTTPException as err:
        logger.error(f"create_new_quiz_setting Error: {err}")
        raise err
    except Exception as err:
        logger.error(f"create_new_quiz_setting Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error in creating QuizSetting",
        )


# Get all QuizSettings
@router.get("", response_model=list[QuizSettingRead])
def get_all_quiz_settings_endpoint(quiz_id: int, db: DBSessionDep):
    """
    Get all QuizSettings
    """
    try:
        return quiz_setting_engine.get_all_quiz_settings_for_quiz(
            db=db, quiz_id=quiz_id
        )
    except Exception as err:
        logger.error(f"get_all_quiz_settings_endpoint Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error in fetching QuizSettings",
        )


# Get a QuizSetting by ID
@router.get("/{quiz_setting_id}", response_model=QuizSettingRead)
def get_quiz_setting_by_id_endpoint(quiz_setting_id: int, db: DBSessionDep):
    """
    Get a QuizSetting by ID
    """
    try:
        return quiz_setting_engine.get_quiz_setting_by_id(
            db=db, quiz_setting_id=quiz_setting_id
        )
    except Exception as err:
        logger.error(f"get_quiz_setting_by_id_endpoint Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QuizSetting not found"
        )


# Update a QuizSetting
@router.patch("/{quiz_setting_id}", response_model=QuizSettingRead)
def update_quiz_setting_endpoint(
    quiz_setting_id: int, quiz_setting_update: QuizSettingUpdate, db: DBSessionDep
):
    """
    Update a QuizSetting
    """
    try:
        quiz_setting = quiz_setting_engine.update_quiz_setting(
            db=db,
            quiz_setting_id=quiz_setting_id,
            quiz_setting_update=quiz_setting_update,
        )
        if not quiz_setting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="QuizSetting not found"
            )
        return quiz_setting
    except Exception as err:
        logger.error(f"update_quiz_setting_endpoint Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error in updating QuizSetting",
        )


# REMOVE QUIZ SETTING
@router.delete("/{quiz_setting_id}")
def remove_quiz_setting_endpoint(quiz_setting_id: int, db: DBSessionDep):
    """
    Remove a QuizSetting
    """
    try:
        return quiz_setting_engine.remove_quiz_setting(
            db=db, quiz_setting_id=quiz_setting_id
        )
    except Exception as err:
        logger.error(f"remove_quiz_setting_endpoint Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QuizSetting not found"
        )
