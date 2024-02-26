
from sqlmodel import Field, SQLModel, Relationship
from datetime import timedelta, datetime
from typing import TYPE_CHECKING, Optional

from app.core.utils.generic_models import QuestionDifficultyEnum, QuestionTypeEnum, BaseIdModel

if TYPE_CHECKING:
    # Avoid circular imports at runtime
    from app.quiz.quiz.models import Quiz
    from app.quiz.question.models import QuestionBank

# ---------------------
# Quiz Attempt Engine (stores the info a user's attempts at a question.)
# ---------------------


# Quiz Attempt Table:
class AnswerSheetBase(SQLModel):
    student_id: int = Field(index=True)
    quiz_id: int = Field(index=True, foreign_key="quiz.id")
    attempted_date: datetime = Field()

    time_limit: timedelta = Field()
    time_start: datetime | None = Field(default=None)
    time_finish: datetime | None = Field(default=None)
    
    total_points: int
    attempt_score: float | None = Field(default=None)
    
    quiz_key: str | None = Field(max_length=160, nullable=True) # TODO: How can we ensure the key added is same as in table except for Runtime Check.

class AnswerSheet(BaseIdModel, AnswerSheetBase, table=True):
    quiz: Optional["Quiz"] = Relationship(back_populates="answer_sheets")
    quiz_answers: list["AnswerSlot"] = Relationship(back_populates="answer_sheet")

    # Relationship to Quiz
    quiz: "Quiz" = Relationship(back_populates="quiz_answer_sheets")

    # TODO: quiz_grades: list["QuizGrade"] = Relationship(back_populates="quiz_attempt")


# Quiz Answer Slot: Save each User Answer and check to update the points awarded
class AnswerSlotBase(SQLModel):
    quiz_answer_sheet_id: int = Field(index=True, foreign_key="answersheet.id")
    question_id: int = Field(index=True, foreign_key="questionbank.id")

    question_type: QuestionTypeEnum

class AnswerSlot(BaseIdModel, AnswerSlotBase, table=True):

    points_awarded: float = Field(default=0)
    answer_sheet: "AnswerSheet" = Relationship(back_populates="quiz_answers")

    question: "QuestionBank" = Relationship(back_populates="quiz_answers")
    selected_options: list["AnswerSlotOption"] = Relationship(
        back_populates="quiz_answer_slot", sa_relationship_kwargs={"lazy": "selectin"})


class AnswerSlotOptionBase(SQLModel):
    quiz_answer_slot_id: int = Field(foreign_key="answerslot.id")
    option_id: int  # This represents the specific option selected


class AnswerSlotOption(BaseIdModel, AnswerSlotOptionBase, table=True):
    # Relationship back to the AnswerSlot
    quiz_answer_slot: "AnswerSlot" = Relationship(
        back_populates="selected_options", sa_relationship_kwargs={"lazy": "joined"})
