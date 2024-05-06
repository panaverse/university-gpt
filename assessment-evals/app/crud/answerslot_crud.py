from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.base import QuestionTypeEnum

from app.models.answerslot_model import  AnswerSlot, AnswerSlotOption, AnswerSlotCreate
from app.core.requests import get_question

class CRUDQuizAnswerSlotEngine:
    # 0. Validate if Quiz Question being attempted is valid Quiz Question and not attemted before
            # Check if answersheet_id and quesion_id are already in the database
    def validate_quiz_question_attempt(
        self, db_session: Session, answersheet_id: int, question_id: int
    ):
        """
        Validate if Quiz Question being attempted is valid Quiz Question and not attemted before
        """
        try:
            db_quiz_answer_slot = db_session.exec(
                select(AnswerSlot).where(
                    AnswerSlot.quiz_answer_sheet_id == answersheet_id,
                    AnswerSlot.question_id == question_id,
                )
            ).one_or_none()

            if db_quiz_answer_slot:
                raise ValueError("Question Already Attempted")

            return True
        except ValueError as e:
            db_session.rollback()
            raise e
        except Exception as e:
            db_session.rollback()
            raise e

    # 1. Create Quiz Answer Slot
    def create_quiz_answer_slot(
        self, db_session: Session, quiz_answer_slot: AnswerSlotCreate
    ):
        """
        Create a Quiz Answer Slot Entry in the Database whenever a student answers a question
        """
        try:
            
            # validate_quiz_question_attempt
            self.validate_quiz_question_attempt(
                db_session=db_session,
                answersheet_id=quiz_answer_slot.quiz_answer_sheet_id,
                question_id=quiz_answer_slot.question_id,
            )
            
            if quiz_answer_slot.selected_options_ids is None:
                raise ValueError("Select MCQ Option to Save It")

            # Prep to add selected_options
            sanitized_selected_options: list[AnswerSlotOption] = []

            for option_id in quiz_answer_slot.selected_options_ids:
                sanitized_selected_options.append(AnswerSlotOption(option_id=option_id))

            db_quiz_answer_slot = AnswerSlot.model_validate(quiz_answer_slot)
            db_quiz_answer_slot.selected_options.extend(sanitized_selected_options)
            db_session.add(db_quiz_answer_slot)

            db_session.commit()
            db_session.refresh(db_quiz_answer_slot)

            return db_quiz_answer_slot
        except ValueError as e:
            db_session.rollback()
            raise e
        except Exception as e:
            db_session.rollback()
            raise e

    # 2. Grade Quiz Answer Slot
    def grade_quiz_answer_slot(
        self, *, db_session: Session, quiz_answer_slot: AnswerSlot
    ):
        """
        Grade a Quiz Answer Slot
        """
        try:
            print("\n\n\n GRADING" "\n\n\n")
            
            if len(quiz_answer_slot.selected_options) == 0:
                print("\n\n\n No Option Selected GRADE IS 0" "\n\n\n")
                quiz_answer_slot.points_awarded = 0
                db_session.add(quiz_answer_slot)
                db_session.commit()
                db_session.refresh(quiz_answer_slot)
                return quiz_answer_slot
            # 1. Get Questions using question_id from question_engine
            question = get_question(
                question_id=quiz_answer_slot.question_id
            )

            # 2.1 for single_select_mcq match answer_id with question.mcq_options and update points_awarded
            if quiz_answer_slot.question_type == QuestionTypeEnum.single_select_mcq:
                
                # Get the correct answer
                selected_option_id = quiz_answer_slot.selected_options[0].option_id
                correct_option_id = next(
                    (option["id"] for option in question["options"] if option["is_correct"]),
                    None,
                )
                if selected_option_id == correct_option_id:
                    quiz_answer_slot.points_awarded = question["points"]
                else:
                    quiz_answer_slot.points_awarded = 0

                db_session.add(quiz_answer_slot)

            # 2.2 for multi_select_mcq match answer_id with question.mcq_options for total correct and matching correct and update points_awarded
            if quiz_answer_slot.question_type == QuestionTypeEnum.multiple_select_mcq:
                print("\n\n\n multi_select_mcq GRADING" "\n\n\n")
                # Get the correct answer
                selected_option_ids = [
                    option.option_id for option in quiz_answer_slot.selected_options
                ]

                print("\n\n\n selected_option_ids", selected_option_ids, "\n\n\n")

                correct_option_ids = [
                    option["id"] for option in question["options"] if option["is_correct"]
                ]

                print("\n\n\n correct_option_ids", correct_option_ids, "\n\n\n")

                # Calculate the number of correctly selected options
                correct_selections = len(
                    set(selected_option_ids) & set(correct_option_ids)
                )
                print(
                    "\n\n\n Calculate the number of correctly selected options \n\n correct_selections",
                    correct_selections,
                    "\n\n\n",
                )
                total_correct_options = len(correct_option_ids)

                print("\n\n\n total_correct_options", total_correct_options, "\n\n\n")

                # Calculate partial points. This could be customized based on  grading policy.
                # For example, award points proportionally based on the number of correctly selected options.
                if correct_selections > 0:
                    partial_points = (
                        correct_selections / total_correct_options
                    ) * question["points"]
                    print("\n\n\n partial_points", partial_points, "\n\n\n")
                    # Round the partial points to two decimal places
                    quiz_answer_slot.points_awarded = round(partial_points, 2)
                else:
                    # No points if no correct options are selected
                    print("\n\n\n No points if no correct options are selected \n\n\n")
                    quiz_answer_slot.points_awarded = 0

                db_session.add(quiz_answer_slot)

            db_session.commit()

            # Refresh the Quiz Answer Slot
            db_session.refresh(quiz_answer_slot)

            return quiz_answer_slot

            # 3. Update Quiz Answer Slot with points_awarded
        except Exception as e:
            db_session.rollback()
            raise e

crud_answer_slot = CRUDQuizAnswerSlotEngine()
