from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

from app.models.base import QuestionTypeEnum, BaseIdModel, QuestionDifficultyEnum
from app.models.answer_models import MCQOption, MCQOptionCreate, MCQOptionRead

if TYPE_CHECKING:
    from app.models.topic_models import Topic
    from app.models.quiz_models import QuizQuestion

# ------------------------------------------------
# QuestionBank Models
# ------------------------------------------------
example_input_question_bank = {
    "topic_id": 1,
    "question_text": "What is a common cause of syntax errors in TypeScript?",
    "is_verified": True,
    "points": 1,
    "difficulty": "easy",
    "question_type": "single_select_mcq",
}

example_output_question_bank = {
    "id": 1,
    "question_text": "What is a common cause of syntax errors in TypeScript?",
    "is_verified": True,
    "points": 1,
    "difficulty": "easy",
    "topic_id": 1,
    "question_type": "single_select_mcq",
    "options": [
        {
            "is_correct": True,
            "option_text": "Missing semicolons at the end of statements",
        },
        {"is_correct": False, "option_text": "Missing types in function parameters"},
    ]
}

example_input_with_options_question_bank = {
    "question_text": "What is a common cause of syntax errors in Dockefile?",
    "is_verified": True,
    "points": 1,
    "difficulty": "easy",
    "topic_id": 1,
    "question_type": "single_select_mcq",
    "options": [
        {
            "is_correct": True,
            "option_text": "Missing BaseImage at the start",
        },
        {"is_correct": False, "option_text": "Add COPY "},
    ]
}


class QuestionBankBase(SQLModel):
    question_text: str
    is_verified: bool = False
    points: int = Field(default=0)
    difficulty: QuestionDifficultyEnum = QuestionDifficultyEnum.easy
    topic_id: int = Field(foreign_key="topic.id")
    question_type: QuestionTypeEnum = Field(default=QuestionTypeEnum.single_select_mcq)

    class Config:
        json_schema_extra = {"example": example_input_question_bank}


class QuestionBank(BaseIdModel, QuestionBankBase, table=True):
    # topic Relationship
    topic: "Topic" = Relationship(back_populates="questions")

    # MCQ Options Relationship
    options: list["MCQOption"] = Relationship(
        back_populates="question", sa_relationship_kwargs={"lazy": "selectin"}
    )

    # QuizQuestion Many to Many Relationship with Join Table
    quiz_questions: list["QuizQuestion"] = Relationship(
        back_populates="question",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class QuestionBankCreate(QuestionBankBase):
    # pass
    options: list["MCQOptionCreate"] = []

    class Config:
        json_schema_extra = {"example": example_input_with_options_question_bank}


class QuestionBankRead(QuestionBankBase):
    id: int
    options: list["MCQOptionRead"] = []


    class Config:
        json_schema_extra = {"example": example_output_question_bank}


class QuestionBankUpdate(SQLModel):
    question_text: str | None = None
    is_verified: bool | None = None
    points: int | None = None
    difficulty: QuestionDifficultyEnum | None = None
    topic_id: int | None = None
