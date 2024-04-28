from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import and_,  select, Session

from app.core.config import logger_config
from app.models.question_models import QuestionBank, QuestionBankCreate
from app.models.answer_models import MCQOption
from app.models.quiz_models import (
    Quiz,
    QuizQuestion,
)

logger = logger_config(__name__)

class CRUDQuizQuestion:
    # 1. Create Quiz Question
    def create_quiz_question(
        self,
        *,
        quiz_id: int,
        quiz_question_create_data: QuestionBankCreate,
        db: Session,
    ):
        try:
            # 0. If quiz_question_create_data.is_verified is False Raise Error
            if not quiz_question_create_data.is_verified:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Question must be verified as True to be added in Quiz",
                )
            # 1. Get the quiz to link the question to
            quiz = db.get(Quiz, quiz_id)
            if not quiz:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
                )

            # 2. Add Question to the QuestionBank then link to the Quiz using QuizQuestion Model
            if quiz_question_create_data.options:
                quiz_question_create_data.options = [
                    MCQOption.model_validate(option)  # type:ignore
                    for option in quiz_question_create_data.options
                ]  # type:ignore

            question_to_db = QuestionBank.model_validate(quiz_question_create_data)

            quiz_question_link = QuizQuestion(
                quiz=quiz, question=question_to_db, topic_id=question_to_db.topic_id
            )

            db.add(quiz_question_link)

            # Update Quiz Sum
            quiz.total_points += question_to_db.points
            db.add(quiz)

            db.commit()
            db.refresh(quiz_question_link)

            return quiz_question_link
        except HTTPException as e:
            db.rollback()
            logger.error(f"create_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in creating Quiz Question",
            )
        except Exception as e:
            db.rollback()
            logger.error(f"create_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in creating Quiz Question",
            )

    # Remove a Quiz Question
    def remove_quiz_question(
        self, *, quiz_id: int, quiz_question_id: int, db: Session
    ):
        try:
            quiz = db.get(Quiz, quiz_id)
            if not quiz:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
                )

            query = (
                select(QuizQuestion)
                .options(
                    selectinload(QuizQuestion.quiz),
                    selectinload(QuizQuestion.question),  # type:ignore
                )
                .where(
                    and_(
                        QuizQuestion.quiz_id == quiz_id,
                        QuizQuestion.question_id == quiz_question_id,
                    )
                )
            )

            quiz_question_row = db.exec(query)
            quiz_question_instance = quiz_question_row.one_or_none()
            print("\n----quiz_question_to_delete----\n", quiz_question_instance)
            if not quiz_question_instance:
                raise ValueError("Quiz Question not found")
            # for quiz_question in quiz_question_instance:

            db.delete(quiz_question_instance)

            # Update Quiz Sum
            quiz.total_points -= quiz_question_instance.question.points
            db.add(quiz)

            db.commit()
            return {"message": "Quiz Question deleted successfully!"}
        except ValueError as e:
            db.rollback()
            logger.error(f"remove_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question not found"
            )
        except Exception as e:
            db.rollback()
            logger.error(f"remove_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in deleting Quiz Question",
            )

    # Rest can be done directly via QUestions Crud API as this is just a link between Quiz and QuestionBank

quiz_question_engine = CRUDQuizQuestion()
