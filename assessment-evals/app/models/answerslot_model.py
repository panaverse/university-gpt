from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

from app.models.base import QuestionTypeEnum, BaseIdModel

if TYPE_CHECKING:
    from app.models.answersheet_model import AnswerSheet

class AnswerSlotBase(SQLModel):
    quiz_answer_sheet_id: int = Field(index=True, foreign_key="answersheet.id")
    question_id: int = Field(index=True)

    question_type: QuestionTypeEnum


class AnswerSlot(BaseIdModel, AnswerSlotBase, table=True):
    points_awarded: float = Field(default=0)
    answer_sheet: "AnswerSheet" = Relationship(back_populates="quiz_answers")

    selected_options: list["AnswerSlotOption"] = Relationship(
        back_populates="quiz_answer_slot", sa_relationship_kwargs={"lazy": "selectin"}
    )


class AnswerSlotCreate(AnswerSlotBase):
    # We will sanitize, append to a new list to extend .selected_options
    selected_options_ids: list[int] = []


class AnswerSlotRead(AnswerSlotBase):
    id: int
    selected_options: list["AnswerSlotOptionBase"] = []


class AnswerSlotUpdate(SQLModel):
    answer_slot_id: int | None = None
    points_awarded: float | None = None


class AnswerSlotOptionBase(SQLModel):
    quiz_answer_slot_id: int = Field(foreign_key="answerslot.id")
    option_id: int  # This represents the specific option selected


class AnswerSlotOption(BaseIdModel, AnswerSlotOptionBase, table=True):
    # Relationship back to the AnswerSlot
    quiz_answer_slot: "AnswerSlot" = Relationship(
        back_populates="selected_options", sa_relationship_kwargs={"lazy": "joined"}
    )
