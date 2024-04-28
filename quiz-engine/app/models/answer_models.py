from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import TYPE_CHECKING
from app.models.base import BaseIdModel

if TYPE_CHECKING:
    from app.models.question_models import QuestionBank

example_input_mcq_option = {
    "option_text": "Missing semicolons at the end of statements",
    "is_correct": True,
    "question_id": 1,
}

example_output_mcq_option = {
    "id": 1,
    "option_text": "Missing semicolons at the end of statements",
    "is_correct": True,
    "question_id": 1,
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z",
}


class MCQOptionBase(SQLModel):
    option_text: str = Field(default=None, max_length=500)
    is_correct: bool = Field(default=False)

    question_id: int | None = Field(foreign_key="questionbank.id", default=None)

    class Config:
        json_schema_extra = {"example": example_input_mcq_option}


class MCQOption(BaseIdModel, MCQOptionBase, table=True):
    # question Relationship
    question: "QuestionBank" = Relationship(
        back_populates="options", sa_relationship_kwargs={"lazy": "joined"}
    ) 


class MCQOptionCreate(MCQOptionBase):
    pass


class MCQOptionRead(MCQOptionBase):
    id: int
    created_at: datetime
    updated_at: datetime


class MCQOptionUpdate(SQLModel):
    option_text: str | None = None
    is_correct: bool | None = None
    question_id: int | None = None