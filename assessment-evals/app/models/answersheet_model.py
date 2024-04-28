from sqlmodel import Field, SQLModel, Relationship
from datetime import timedelta, datetime
from typing import TYPE_CHECKING
from app.models.base import BaseIdModel, QuizAttemptStatus

if TYPE_CHECKING:
    from app.models.answerslot_model import AnswerSlot


class AnswerSheetBase(SQLModel):
    student_id: int = Field(index=True)
    quiz_id: int = Field(index=True)

    time_limit: timedelta = Field()
    time_start: datetime | None = Field(default=None)
    time_finish: datetime | None = Field(default=None)
    status: QuizAttemptStatus | None = Field(default=QuizAttemptStatus.in_progress)

    total_points: int
    attempt_score: float | None = Field(default=None)

    quiz_key: str | None = Field(
        max_length=160, nullable=True
    )  # TODO: How can we ensure the key added is same as in table except for Runtime Check.


class AnswerSheet(BaseIdModel, AnswerSheetBase, table=True):
    quiz_answers: list["AnswerSlot"] = Relationship(back_populates="answer_sheet")

    # TODO: quiz_grades: list["QuizGrade"] = Relationship(back_populates="quiz_attempt")


class AnswerSheetCreate(SQLModel):
    student_id: int
    quiz_id: int
    time_limit: timedelta
    time_start: datetime
    total_points: int
    quiz_key: str


class AnswerSheetUpdate(SQLModel):
    time_finish: datetime | None = None
    attempt_score: float | None = None
    status: QuizAttemptStatus | None = None


class AnswerSheetRead(AnswerSheetBase):
    id: int



class AttemptQuizRequest(SQLModel):
    student_id: int
    quiz_id: int
    quiz_key: str
