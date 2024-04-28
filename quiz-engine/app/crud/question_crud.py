from fastapi import HTTPException, status
from sqlmodel import select, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.question_models import (
    QuestionBank,
    QuestionBankCreate,
    QuestionBankUpdate,
    MCQOption,
)
from app.core.config import logger_config
from app.crud.topic_crud import topic_crud
logger = logger_config(__name__)


class QuestionCRUD:
    def add_question(self, *, question: QuestionBankCreate, db: Session):
        """
        Add a question to the database.

        Args:
            question (QuestionBank): The question object to be added.
            db (Session): The database session.

        Returns:
            QuestionBank: The added question.

        """
        try:
            if question.options:
                question.options = [
                    MCQOption.model_validate(option)
                    for option in question.options  # type: ignore
                ]
            db_question = QuestionBank.model_validate(question)

            db.add(db_question)
            db.commit()
            db.refresh(db_question)
            return db_question
        except IntegrityError as e:
            db.rollback()  # Ensure rollback is awaited
            logger.error(
                f"ADD_Question: An integrity error occurred while adding the Question: {e}"
            )
            raise HTTPException(status_code=500, detail="Data integrity issue.")

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(
                f"ADD_Question: A database error occurred while adding the Question: {e}"
            )
            raise HTTPException(status_code=500, detail="Database operation failed.")

        except Exception as e:
            db.rollback()
            logger.error(f"ADD_Question: An unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    def read_questions(self, *, db: Session, offset: int, limit: int):
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
            result = db.exec(select(QuestionBank).offset(offset).limit(limit))
            questions = result.all()
            if not questions:
                raise ValueError("No questions found")
            return questions
        except ValueError as e:
            logger.error(f"READ_Questions: No questions found: {e}")
            db.rollback()
            raise HTTPException(status_code=404, detail="No questions found")
        except SQLAlchemyError as e:
            logger.error(
                f"READ_Questions: A database error occurred while reading the Questions: {e}"
            )
            db.rollback()
            raise HTTPException(status_code=500, detail="Database operation failed.")
        except Exception as e:
            logger.error(f"READ_Questions: An unexpected error occurred: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    def read_questions_by_type(self, *, question_type: str, db: Session):
        """
        Get all questions of a specific question type from the database.

        Args:
            question_type (str): The name of the question type.
            db (Session): The database session.

        Returns:
            List[QuestionBank]: The list of questions.

        """

        try:
            result = db.exec(
                select(QuestionBank).where(QuestionBank.question_type == question_type)
            )
            questions = result.all()

            if not questions:
                raise ValueError("questions not found")
            return questions

        except ValueError as e:
            db.rollback()  # Ensure rollback is awaited
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No questions found"
            ) from e

        except SQLAlchemyError as e:
            db.rollback()  # Ensure rollback is awaited
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            ) from e

        except Exception as e:
            db.rollback()  # Ensure rollback is awaited
            raise Exception("An unexpected error occurred.") from e

    def get_question_by_id(self, *, id: int, db: Session):
        """
        Get a question by its ID from the database.

        Args:
            id (int): The ID of the question.
            db (Session): The database session.

        Returns:
            QuestionBank: The retrieved question.

        """

        try:
            # question = db.get(QuestionBank, id)
            result = db.exec(select(QuestionBank).where(QuestionBank.id == id))
            question = result.first()
            if not question:
                raise ValueError("Question not found")
            return question
        except ValueError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            ) from e
        except Exception as e:
            db.rollback()
            raise Exception("An unexpected error occurred.") from e

    def update_question(
        self, *, id: int, question: QuestionBankUpdate, db: Session
    ):
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
            question_to_update = db.get(QuestionBank, id)
            if not question_to_update:
                raise ValueError("Question not found")
            question_data = question.model_dump(exclude_unset=True)
            question_to_update.sqlmodel_update(question_data)
            db.add(question_to_update)
            db.commit()
            db.refresh(question_to_update)
            return question_to_update
        except ValueError:
            db.rollback()
            logger.error("UPDATE_Question: Question not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"UPDATE_Question: Error updating question: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            ) from e
        except Exception as e:
            db.rollback()
            logger.error(f"UPDATE_Question: Error updating question: {str(e)}")
            raise Exception("Error updating question")

    def delete_question(self, *, id: int, db: Session):
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
            question = db.get(QuestionBank, id)
            if not question:
                raise ValueError("Question not found")
            db.delete(question)
            db.commit()
            return {"message": "Question deleted successfully"}
        except HTTPException:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            ) from e

    # Get All Questions for a Topic
    # Takes topic_id 
    # 1. Check if topic_id is valid
    def get_questions_by_topic(self, *, topic_id: int, db: Session):
        """
        Get all questions for a topic from the database.

        Args:
            topic_id (int): The ID of the topic.
            db (Session): The database session.

        Returns:
            List[QuestionBank]: The list of questions.

        """

        try:
            topic_check = topic_crud.read_topic_by_id(id=topic_id, db=db)
            if not topic_check:
                raise ValueError("Topic not found")

            result = db.exec(
                select(QuestionBank).where(QuestionBank.topic_id == topic_id)
            )
            questions = result.all()

            if not questions:
                raise ValueError("questions not found")
            return questions

        except ValueError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No questions found"
            ) from e
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            ) from e
        

question_crud = QuestionCRUD()
