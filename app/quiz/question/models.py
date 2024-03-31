from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import TYPE_CHECKING

from app.core.utils.generic_models import QuestionDifficultyEnum, QuestionTypeEnum, BaseIdModel

if TYPE_CHECKING:
    from app.quiz.topic.models import Topic
    from app.quiz.quiz.models import QuizQuestion
    from app.quiz.answersheet.models import AnswerSlot

#------------------------------------------------
            #MCQOption Models   
#------------------------------------------------
    
example_input_mcq_option = {
    "option_text": "Missing semicolons at the end of statements",
    "is_correct": True,
    "question_id": 1
}

example_output_mcq_option = {
    "id": 1,
    "option_text": "Missing semicolons at the end of statements",
    "is_correct": True,
    "question_id": 1,
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z"
}

class MCQOptionBase(SQLModel):
    option_text: str = Field(default=None, max_length=500)
    is_correct: bool = Field(default=False)

    question_id: int | None = Field(foreign_key='questionbank.id', default=None)

    class Config:
        json_schema_extra = {"example": example_input_mcq_option}


class MCQOption(BaseIdModel, MCQOptionBase, table=True):

    # question Relationship
    question: "QuestionBank" = Relationship(back_populates='options', sa_relationship_kwargs={"lazy": "joined"})  # type: ignore


class MCQOptionCreate(MCQOptionBase):
    pass


class MCQOptionRead(MCQOptionBase):
    id: int
    created_at: datetime
    updated_at: datetime


class MCQOptionUpdate(MCQOptionBase):
    option_text: str | None = None
    is_correct: bool | None = None
    question_id: int | None = None

#------------------------------------------------
            #QuestionBank Models
#------------------------------------------------
example_input_question_bank = {
    "topic_id": 1,
    "question_text": "What is a common cause of syntax errors in TypeScript?",
    "is_verified": True,
    "points": 1,
    "difficulty": "easy",
    "question_type": "single_select_mcq"
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
                    {"is_correct": True, "option_text": "Missing semicolons at the end of statements"},
                    {"is_correct": False, "option_text": "Missing types in function parameters"}],
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z"
}
class QuestionBankBase(SQLModel):
    question_text: str
    is_verified: bool = False
    points: int = Field(default=0)
    difficulty: QuestionDifficultyEnum = QuestionDifficultyEnum.easy
    topic_id: int = Field(foreign_key='topic.id')
    question_type: QuestionTypeEnum = Field(default=QuestionTypeEnum.single_select_mcq)

    class Config:
        json_schema_extra = {
            "example": example_input_question_bank
        }


class QuestionBank(BaseIdModel, QuestionBankBase, table=True):

    # topic Relationship
    topic: 'Topic' = Relationship(back_populates='questions')

    # MCQ Options Relationship
    options: list['MCQOption'] = Relationship(back_populates='question', sa_relationship_kwargs={"lazy": "selectin"})

    # QuizQuestion Many to Many Relationship with Join Table
    quiz_questions: list['QuizQuestion'] = Relationship(back_populates="question", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    quiz_answers: list['AnswerSlot'] = Relationship(back_populates="question")


class QuestionBankCreate(QuestionBankBase):
    # pass
    options: list["MCQOptionCreate"] = []

    class Config:
        json_schema_extra = {
            "example": example_output_question_bank
        }


class QuestionBankRead(QuestionBankBase):
    id: int
    options: list['MCQOptionRead'] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": example_output_question_bank
        }


class QuestionBankUpdate(QuestionBankBase):
    question_text: str | None = None
    is_verified: bool | None = None
    points: int | None = None
    difficulty: QuestionDifficultyEnum | None = None
    topic_id: int | None = None