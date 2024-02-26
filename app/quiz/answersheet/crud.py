from sqlmodel import select, func, and_
from app.core.database import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.engine.result import ScalarResult
from datetime import datetime

from app.quiz.answersheet.models import (AnswerSheet, AnswerSlot, AnswerSlotOption, 
                                         AnswerSheetCreate, AnswerSheetUpdate, AnswerSheetRead, 
                                         AnswerSlotCreate, AnswerSlotUpdate, AnswerSlotRead)
from app.quiz.question.crud import get_question_by_id


class CRUDQuizAnswerSheetEngine:
    # 1. Create Quiz Attempt
    async def create_answer_sheet(self, db_session: AsyncSession, answer_sheet_obj_in: AnswerSheetCreate):
        """
        Create an Answer Sheet Entry in the Database whenever a student attempts a quiz
        """
        try:
            db_quiz_attempt = AnswerSheet.model_validate(answer_sheet_obj_in)
            db_session.add(db_quiz_attempt)
            await db_session.commit()
            await db_session.refresh(db_quiz_attempt)
            return db_quiz_attempt
        except Exception as e:
            await db_session.rollback()
            raise e

    # 2. Get  Answer Sheet by ID
    async def get_answer_sheet_by_id(self, db_session: AsyncSession, answer_sheet_id: int):
        """
        Get  Answer Sheet by ID
        """
        return await db_session.get(AnswerSheet, answer_sheet_id)

    # Check if time_limit + time_start is greater than current time
    async def is_answer_sheet_active(self, db_session: AsyncSession, answer_sheet_id: int):
        """
        Check if the  Answer Sheet is still active
            If yes, then the quiz is still active and return True
            If not add time_finish to quiz_id and return False
        """

        answer_sheet_obj = await self.get_answer_sheet_by_id(db_session=db_session, answer_sheet_id=answer_sheet_id)
        if not answer_sheet_obj:
            raise ValueError("Invalid Quiz Attempt ID")

        # Calculate the end time of the quiz
        end_time = answer_sheet_obj.time_start + answer_sheet_obj.time_limit

        # Check if current UTC time is past the end time
        if datetime.utcnow() < end_time:
            print("\n-----Quiz is still active----\n")
            return True
        else:
            print("\n-----Quiz is not active----\n")
            answer_sheet_obj.time_finish = datetime.utcnow()
            await db_session.commit()
            return False

    # Lock the quiz
    async def finish_answer_sheet_attempt(self, db_session: AsyncSession, answer_sheet_id: int):
        """
        Lock the Answer Sheet 
        """
        # 1. Load the Answer Sheet with AnswerSlot
        answer_sheet_obj_exec = await db_session.execute(select(AnswerSheet).options(selectinload(AnswerSheet.quiz_answers)).where(AnswerSheet.id == answer_sheet_id))
        answer_sheet_obj = answer_sheet_obj_exec.one_or_none()

        if not answer_sheet_obj:
            raise ValueError("Invalid Quiz Attempt ID")

        print("\n-----answer_sheet_obj----\n", answer_sheet_obj)
        print("\n-----quiz_answers----\n", answer_sheet_obj.quiz_answers)

        # 2. Add Finish Time to Quiz Attempt if not already added
        if not answer_sheet_obj.time_finish:
            answer_sheet_obj.time_finish = datetime.utcnow()
            await db_session.commit()

        # 3. Grade & Count
        # 3.1 Check if any Quiz Answer Slot is not graded
        for answer_slot in answer_sheet_obj.quiz_answers:
            if not answer_slot.points_awarded:
                await crud_answer_slot.grade_quiz_answer_slot(db_session=db_session, quiz_answer_slot=answer_slot)

        # 4. Calculate the total score
        # A Query that returns the sum of points_awarded for all quiz_answer_slots
        attempt_score_exec: ScalarResult = await db_session.execute(select(func.sum(AnswerSlot.points_awarded)).where(AnswerSlot.quiz_answer_sheet_id == answer_sheet_id))
        attempt_score: float | None = attempt_score_exec.one_or_none()

        if attempt_score is None:
            attempt_score = 0

        print("\n-----attempt_score----\n", attempt_score)

        # 5. Update the Quiz Attempt with attempt_score
        answer_sheet_obj.attempt_score = attempt_score
        await db_session.commit()
        await db_session.refresh(answer_sheet_obj)

        return answer_sheet_obj

    # Get Quiz Attempt Based on User ID and Quiz ID
    async def get_answer_sheet_by_user_id_and_quiz_id(self, db_session: AsyncSession, user_id: str, quiz_id: int):
        """
        Get Quiz Attempt by User ID and Quiz ID
        """
        print("\n-----user_id----\n", user_id)
        print("\n-----quiz_id----\n", quiz_id)

        quiz_answer_sheet = await db_session.execute(select(AnswerSheet.id).where(and_(AnswerSheet.user_id == user_id, AnswerSheet.quiz_id == quiz_id)))
        quiz_answer_sheet_obj = quiz_answer_sheet.one_or_none()

        print("\n-----attempt_quiz_ret----\n", quiz_answer_sheet_obj)
        
        return quiz_answer_sheet_obj

    # Ensure student have not attempted the quiz before
    async def student_answer_sheet_exists(self, db_session: AsyncSession, user_id: str, quiz_id: int):

        answer_sheet_query = await db_session.execute(select(AnswerSheet.id).where(and_(AnswerSheet.student_id == user_id, AnswerSheet.quiz_id == quiz_id)))
        answer_sheet_obj = answer_sheet_query.one_or_none()

        if answer_sheet_obj:
            return True
        
        return False

class CRUDQuizAnswerSlotEngine:
    # 1. Create Quiz Answer Slot
    async def create_quiz_answer_slot(self, db_session: AsyncSession, quiz_answer_slot: AnswerSlotCreate):
        """
        Create a Quiz Answer Slot Entry in the Database whenever a student answers a question
        """
        try:
            if quiz_answer_slot.selected_options_ids is None:
                raise ValueError("Select MCQ Option to Save It")

            # Prep to add selected_options
            sanitized_selected_options: list[AnswerSlotOption] = []

            for option_id in quiz_answer_slot.selected_options_ids:
                sanitized_selected_options.append(AnswerSlotOption(option_id=option_id))

            db_quiz_answer_slot = AnswerSlot.model_validate(quiz_answer_slot)
            db_quiz_answer_slot.selected_options.extend(sanitized_selected_options)
            db_session.add(db_quiz_answer_slot)
            
            await db_session.commit()
            await db_session.refresh(db_quiz_answer_slot)
            
            return db_quiz_answer_slot
        except Exception as e:
            await db_session.rollback()
            raise e

    # 2. Grade Quiz Answer Slot
    async def grade_quiz_answer_slot(self, db_session: AsyncSession, quiz_answer_slot: AnswerSlot):
        """
        Grade a Quiz Answer Slot
        """
        try:
            # 1. Get Questions using question_id from question_engine
            question = await get_question_by_id(db_session=db_session, id=quiz_answer_slot.question_id)

            # 2.1 for single_select_mcq match answer_id with question.mcq_options and update points_awarded
            if quiz_answer_slot.question_type == "single_select_mcq":
                # Get the correct answer
                selected_option_id = quiz_answer_slot.selected_options[0].option_id
                correct_option_id = next((option.id for option in question.mcq_options if option.is_correct), None)
                if selected_option_id == correct_option_id:
                    quiz_answer_slot.points_awarded = question.points
                else:
                    quiz_answer_slot.points_awarded = 0

                db_session.add(quiz_answer_slot)
                await db_session.commit()

            # 2.2 for multi_select_mcq match answer_id with question.mcq_options for total correct and matching correct and update points_awarded
            if quiz_answer_slot.question_type == "multi_select_mcq":
                # Get the correct answer
                selected_option_ids = [option.option_id for option in quiz_answer_slot.selected_options]

                correct_option_ids = [option.id for option in question.mcq_options if option.is_correct]

                # Calculate the number of correctly selected options
                correct_selections = len(set(selected_option_ids) & set(correct_option_ids))
                total_correct_options = len(correct_option_ids)

                # Calculate partial points. This could be customized based on  grading policy.
                # For example, award points proportionally based on the number of correctly selected options.
                if correct_selections > 0:
                    partial_points = (correct_selections / total_correct_options) * question.points
                    quiz_answer_slot.points_awarded = round(partial_points, 2)  # Round the partial points to two decimal places
                else:
                    quiz_answer_slot.points_awarded = 0  # No points if no correct options are selected


                db_session.add(quiz_answer_slot)
                await db_session.commit()

            # Refresh the Quiz Answer Slot
            await db_session.refresh(quiz_answer_slot)
            return quiz_answer_slot

            # 3. Update Quiz Answer Slot with points_awarded
        except Exception as e:
            await db_session.rollback()
            raise e


crud_answer_sheet = CRUDQuizAnswerSheetEngine()

crud_answer_slot = CRUDQuizAnswerSlotEngine()
