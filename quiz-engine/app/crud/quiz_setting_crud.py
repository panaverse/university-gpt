from datetime import datetime

from fastapi import HTTPException
from sqlmodel import and_, select, Session

from app.core.config import logger_config

from app.models.quiz_setting import (
    QuizSetting,
    QuizSettingCreate,
    QuizSettingUpdate,

)
from app.models.quiz_models import Quiz

logger = logger_config(__name__)


class CRUDQuizSetting:
    def create_quiz_setting(
        self, *, db: Session, quiz_setting: QuizSettingCreate
    ):
        """
        Create a new QuizSetting in the database
        """
        try:
            # If quiz_key is already used for the quiz, raise an HTTPException
            check_quiz_setting = db.exec(
                select(QuizSetting).where(
                    and_(
                        QuizSetting.quiz_id == quiz_setting.quiz_id,
                        QuizSetting.quiz_key == quiz_setting.quiz_key,
                    )
                )
            ).all()
            
            if len(check_quiz_setting) >=1:
                raise HTTPException(
                    status_code=400,
                    detail="Quiz Key already used for the quiz",
                )
            
            
            # Create a new QuizSetting
            # Convert start_time and end_time to offset-naive datetime objects if they are not None
            # if quiz_setting.start_time and quiz_setting.start_time.tzinfo:
            #     quiz_setting.start_time = quiz_setting.start_time.replace(tzinfo=None)

            # if quiz_setting.end_time and quiz_setting.end_time.tzinfo:
            #     quiz_setting.end_time = quiz_setting.end_time.replace(tzinfo=None)

            db_quiz_setting = QuizSetting.model_validate(quiz_setting)

            print("\n----db_quiz_setting----\n", db_quiz_setting)

            # Add the new QuizSetting to the database
            db.add(db_quiz_setting)

            # Commit the session to the database to actually add the QuizSetting
            db.commit()

            # Refresh the database to get the updated details of the QuizSetting
            db.refresh(db_quiz_setting)

            # Return the newly created QuizSetting
            return db_quiz_setting
        except HTTPException as http_err:
            db.rollback()
            raise http_err
        except Exception as e:
            db.rollback()
            logger.error(f"create_quiz_setting Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Get all QuizSettings for a quiz
    def get_all_quiz_settings_for_quiz(self, *, db: Session, quiz_id: int):
        """
        Get all QuizSettings from the database
        """
        try:
            quiz_settings = db.exec(
                select(QuizSetting).where(and_(QuizSetting.quiz_id == quiz_id))
            )
            # Return all QuizSettings
            return quiz_settings.all()

        except Exception as e:
            db.rollback()
            logger.error(f"get_all_quiz_settings_for_quiz Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Get a QuizSetting by ID
    def get_quiz_setting_by_id(
        self, *, db: Session, quiz_setting_id: int
    ) -> QuizSetting:
        """
        Get a QuizSetting from the database by ID
        """
        try:
            quiz_setting = db.get(QuizSetting, quiz_setting_id)

            # If the QuizSetting doesn't exist, raise an HTTPException
            if quiz_setting is None:
                raise HTTPException(status_code=404, detail="QuizSetting not found")

            # Return the QuizSetting
            return quiz_setting
        except Exception as e:
            db.rollback()
            logger.error(f"get_quiz_setting_by_id Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Update a QuizSetting
    def update_quiz_setting(
        self,
        *,
        db: Session,
        quiz_setting_id: int,
        quiz_setting_update: QuizSettingUpdate,
    ) -> QuizSetting:
        """
        Update a QuizSetting in the database
        """
        try:
            db_quiz_setting = db.get(QuizSetting, quiz_setting_id)

            if db_quiz_setting is None:
                raise HTTPException(status_code=404, detail="QuizSetting not found")

            update_data = quiz_setting_update.model_dump(exclude_unset=True)

            db_quiz_setting.sqlmodel_update(update_data)

            db.commit()
            db.refresh(db_quiz_setting)
            return db_quiz_setting
        except Exception as e:
            db.rollback()
            logger.error(f"update_quiz_setting Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Remove a QUiz Setting
    def remove_quiz_setting(
        self, *, db: Session, quiz_setting_id: int
    ) -> dict:
        """
        Remove a QuizSetting from the database
        """
        try:
            db_quiz_setting = db.get(QuizSetting, quiz_setting_id)

            if db_quiz_setting is None:
                raise HTTPException(status_code=404, detail="QuizSetting not found")

            db.delete(db_quiz_setting)
            db.commit()
            return {"message": "QuizSetting deleted successfully!"}
        except Exception as e:
            db.rollback()
            logger.error(f"remove_quiz_setting Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Check Is Key Valid
    def validate_quiz_key(self, *, db: Session, quiz_id: int, quiz_key: str):
        """
        Check if the Quiz Key is valid
        """
        try:
            quiz_setting_statement = db.exec(
                select(QuizSetting).where(
                    and_(
                        QuizSetting.quiz_id == quiz_id, QuizSetting.quiz_key == quiz_key
                    )
                )
            )
            quiz_setting = quiz_setting_statement.one_or_none()

            if quiz_setting is None:
                raise HTTPException(status_code=404, detail="QuizSetting not found")

            # If Time is not None then check if it is between start and end time
            if quiz_setting.start_time and quiz_setting.end_time:
                if (
                    not quiz_setting.start_time
                    <= datetime.now()
                    <= quiz_setting.end_time
                ):
                    raise HTTPException(status_code=404, detail="Quiz is not active")

            return quiz_setting
        except HTTPException as httperr:
            db.rollback()
            logger.error(f"is_quiz_key_valid Error: {httperr}")
            raise httperr
        except Exception as e:
            db.rollback()
            logger.error(f"is_quiz_key_valid Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))



quiz_setting_engine = CRUDQuizSetting()