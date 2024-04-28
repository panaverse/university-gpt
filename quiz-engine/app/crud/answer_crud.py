from fastapi import HTTPException
from sqlmodel import select, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.answer_models import (
    MCQOption,
    MCQOptionCreate,
    MCQOptionUpdate,
)
from app.models.question_models import QuestionBank
from app.core.config import logger_config

logger = logger_config(__name__)


# Add MCQ Option to the Database
class MCQCRUD:
    def add_mcq_option(
        self, *, mcq_option: MCQOptionCreate, session: Session
    ):
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
            session.commit()
            session.refresh(db_mcq_option)
            return db_mcq_option
        except IntegrityError as e:
            session.rollback()
            logger.error(
                f"ADD_MCQ_Option: An integrity error occurred while adding the MCQ Option: {e}"
            )
            raise HTTPException(status_code=500, detail="Data integrity issue.")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(
                f"ADD_MCQ_Option: A database error occurred while adding the MCQ Option: {e}"
            )
            raise HTTPException(status_code=500, detail="Database operation failed.")
        except Exception as e:
            session.rollback()
            logger.error(f"ADD_MCQ_Option: An unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    def read_mcq_options(self, *, db: Session, offset: int, limit: int):
        try:
            mcq_options = db.exec(select(MCQOption).offset(offset).limit(limit)).all()
            if not mcq_options:
                raise ValueError("No MCQ options found")
            return mcq_options
        except ValueError as e:
            logger.error(f"READ_MCQ_Options: No MCQ options found: {e}")
            db.rollback()
            raise HTTPException(status_code=404, detail="No MCQ options found")
        except SQLAlchemyError as e:
            logger.error(
                f"READ_MCQ_Options: A database error occurred while reading the MCQ Options: {e}"
            )
            db.rollback()
            raise HTTPException(status_code=500, detail="Database operation failed.")
        except Exception as e:
            logger.error(f"READ_MCQ_Options: An unexpected error occurred: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    def get_mcq_option_by_id(self, *, id: int, db: Session):
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
            mcq_option = db.get(MCQOption, id)
            if not mcq_option:
                raise ValueError("MCQ Option not found")
            return mcq_option
        except ValueError as e:
            db.rollback()
            logger.error(f"GET_MCQ_Option: MCQ Option not found: {e}")
            raise HTTPException(status_code=404, detail="MCQ Option not found")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(
                f"GET_MCQ_Option: A database error occurred while retrieving the MCQ Option: {e}"
            )
            raise HTTPException(status_code=500, detail="Database operation failed.")
        except Exception as e:
            db.rollback()
            logger.error(f"GET_MCQ_Option: An unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    def update_mcq_option(
        self, *, id: int, mcq_option: MCQOptionUpdate, db: Session
    ):
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
            mcq_option_to_update = db.get(MCQOption, id)
            if not mcq_option_to_update:
                raise ValueError("MCQ Option not found")
            mcq_option_data = mcq_option.model_dump(exclude_unset=True)
            for key, value in mcq_option_data.items():
                setattr(mcq_option_to_update, key, value)
            db.add(mcq_option_to_update)
            db.commit()
            db.refresh(mcq_option_to_update)
            return mcq_option_to_update
        except ValueError as e:
            db.rollback()
            logger.error(f"UPDATE_MCQ_Option: MCQ Option not found: {e}")
            raise HTTPException(status_code=404, detail="MCQ Option not found")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"UPDATE_MCQ_Option: Error updating MCQ Option: {str(e)}")
            raise HTTPException(status_code=500, detail="Database operation failed.")
        except Exception as e:
            db.rollback()
            logger.error(f"UPDATE_MCQ_Option: An unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    def delete_mcq_option(self, *, id: int, db: Session):
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
            mcq_option = db.get(MCQOption, id)
            if not mcq_option:
                raise ValueError("MCQ Option not found")
            db.delete(mcq_option)
            db.commit()
            return {"message": "MCQ Option deleted successfully"}
        except ValueError as e:
            db.rollback()
            logger.error(f"DELETE_MCQ_Option: MCQ Option not found: {e}")
            raise HTTPException(status_code=404, detail="MCQ Option not found")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"DELETE_MCQ_Option: Error deleting MCQ Option: {str(e)}")
            raise HTTPException(status_code=500, detail="Database operation failed.")
        except Exception as e:
            db.rollback()
            logger.error(f"DELETE_MCQ_Option: An unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    # Get all mcq options for a question_id
    def get_mcq_options_by_question_id(self, *, question_id: int, db: Session):
        try:
            # Firstly verify Question ID
            question = db.get(QuestionBank, question_id)
            if question is None:
                raise ValueError("Question not found")
            mcq_options = db.exec(
                select(MCQOption).where(MCQOption.question_id == question_id)
            ).all()
            if not mcq_options:
                raise ValueError("No MCQ options found")
            return mcq_options
        except ValueError as e:
            logger.error(f"GET_MCQ_Options: No MCQ options found: {e}")
            db.rollback()
            raise HTTPException(status_code=404, detail="No MCQ options found")
        except SQLAlchemyError as e:
            logger.error(
                f"GET_MCQ_Options: A database error occurred while reading the MCQ Options: {e}"
            )
            db.rollback()
            raise HTTPException(status_code=500, detail="Database operation failed.")
        except Exception as e:
            logger.error(f"GET_MCQ_Options: An unexpected error occurred: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")


mcq_crud = MCQCRUD()
