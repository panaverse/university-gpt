from datetime import datetime
from sqlmodel import select, func, and_, Session
from sqlalchemy.orm import selectinload

# from app.crud.question_crud import question_crud
from app.models.base import QuizAttemptStatus
from app.models.answersheet_model import (
    AnswerSheet,
    AnswerSheetCreate,
)
from app.models.answerslot_model import  AnswerSlot
from app.crud.answerslot_crud import crud_answer_slot

# TODO: Test and Remove it
from sqlalchemy.engine.result import ScalarResult

class CRUDQuizAnswerSheetEngine:
    def create_answer_sheet(
        self, *, db_session: Session, answer_sheet_obj_in: AnswerSheetCreate
    ):
        """
        Create an Answer Sheet Entry in the Database whenever a student attempts a quiz
        """
        try:
            # Convert start_time and end_time to offset-naive datetime objects if they are not None
            # if answer_sheet_obj_in.time_start and answer_sheet_obj_in.time_start.tzinfo:
            #     answer_sheet_obj_in.time_start = answer_sheet_obj_in.time_start.replace(
            #         tzinfo=None
            #     )

            db_quiz_attempt = AnswerSheet.model_validate(answer_sheet_obj_in)
            print("\n---db_quiz_attempt---\n", db_quiz_attempt)
            db_session.add(db_quiz_attempt)
            db_session.commit()
            db_session.refresh(db_quiz_attempt)
            return db_quiz_attempt
        except Exception as e:
            db_session.rollback()
            raise e

    def get_answer_sheet_by_id(
        self, db_session: Session, answer_sheet_id: int, student_id: int
    ):
        """
        Get  Answer Sheet by ID
        """

        answer_sheet_query = db_session.exec(
            select(AnswerSheet).where(
                and_(
                    AnswerSheet.id == answer_sheet_id,
                    AnswerSheet.student_id == student_id,
                )
            )
        )
        answer_sheet_obj = answer_sheet_query.one_or_none()

        return answer_sheet_obj

    def is_answer_sheet_active(
        self, db_session: Session, answer_sheet_id: int, student_id: int
    ):
        """
        Check if the  Answer Sheet is still active
            If yes, then the quiz is still active and return True
            If not add time_finish to quiz_id and return False
        """

        answer_sheet_obj = self.get_answer_sheet_by_id(
            db_session=db_session,
            answer_sheet_id=answer_sheet_id,
            student_id=student_id,
        )
        if not answer_sheet_obj:
            raise ValueError("Invalid Quiz Attempt ID")

        if answer_sheet_obj.status == QuizAttemptStatus.completed:
            print("\n-----Quiz is already completed----\n")
            return False

        if answer_sheet_obj.status == QuizAttemptStatus.in_progress:
            print("\n-----Quiz is in progress----\n")
            # 1. Check if the quiz time limit is ended

            # Calculate the end time of the quiz
            end_time = answer_sheet_obj.time_start + answer_sheet_obj.time_limit

            # Check if current UTC time is past the end time
            if datetime.utcnow() < end_time:
                print("\n-----Quiz is still active----\n")
                return True
            else:
                print("\n-----Quiz is not active----\n")
                answer_sheet_obj.time_finish = datetime.utcnow()
                answer_sheet_obj.status = QuizAttemptStatus.completed
                db_session.commit()
                return False

    def finish_answer_sheet_attempt(
        self, db_session: Session, answer_sheet_id: int
    ):
        """
        Lock the Answer Sheet
        """
        # 1. Load the Answer Sheet with AnswerSlot
        answer_sheet_obj_exec = db_session.exec(
            select(AnswerSheet)
            .options(selectinload(AnswerSheet.quiz_answers))  # type:ignore
            .where(AnswerSheet.id == answer_sheet_id)
        )  # type:ignore
        answer_sheet_obj = answer_sheet_obj_exec.one_or_none()

        if not answer_sheet_obj:
            raise ValueError("Invalid Quiz Attempt ID")

        print("\n-----answer_sheet_obj----\n", answer_sheet_obj)

        # 2. Add Finish Time to Quiz Attempt if not already added
        if not answer_sheet_obj.time_finish:
            answer_sheet_obj.time_finish = datetime.utcnow()
            answer_sheet_obj.status = QuizAttemptStatus.completed
            db_session.commit()

        # 3. Grade & Count
        # 3.1 Check if any Quiz Answer Slot is not graded
        for answer_slot in answer_sheet_obj.quiz_answers:
            if not answer_slot.points_awarded:
                crud_answer_slot.grade_quiz_answer_slot(
                    db_session=db_session, quiz_answer_slot=answer_slot
                )

        # 4. Calculate the total score
        # A Query that returns the sum of points_awarded for all quiz_answer_slots
        attempt_score_exec: ScalarResult = db_session.exec(
            select(func.sum(AnswerSlot.points_awarded)).where(
                AnswerSlot.quiz_answer_sheet_id == answer_sheet_id
            )
        )
        attempt_score: float | None = attempt_score_exec.one_or_none()

        if attempt_score is None:
            attempt_score = 0

        print("\n-----attempt_score----\n", attempt_score)

        # 5. Update the Quiz Attempt with attempt_score
        answer_sheet_obj.attempt_score = attempt_score

        db_session.commit()
        db_session.refresh(answer_sheet_obj)

        return answer_sheet_obj

    def get_answer_sheet_by_user_id_and_quiz_id(
        self, db_session: Session, user_id: str, quiz_id: int
    ):
        """
        Get Quiz Attempt by User ID and Quiz ID
        """
        print("\n-----user_id----\n", user_id)
        print("\n-----quiz_id----\n", quiz_id)

        quiz_answer_sheet = db_session.exec(
            select(AnswerSheet.id).where(
                and_(AnswerSheet.student_id == user_id, AnswerSheet.quiz_id == quiz_id)
            )
        )
        quiz_answer_sheet_obj = quiz_answer_sheet.one_or_none()

        print("\n-----attempt_quiz_ret----\n", quiz_answer_sheet_obj)

        return quiz_answer_sheet_obj

    def student_answer_sheet_exists(
        self, db_session: Session, user_id: int, quiz_id: int
    ):
        answer_sheet_query = db_session.exec(
            select(AnswerSheet).where(
                and_(AnswerSheet.student_id == user_id, AnswerSheet.quiz_id == quiz_id)
            )
        )
        answer_sheet_obj = answer_sheet_query.one_or_none()

        return answer_sheet_obj



crud_answer_sheet = CRUDQuizAnswerSheetEngine()