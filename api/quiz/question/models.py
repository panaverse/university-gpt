from sqlmodel import Field, Relationship, SQLModel, Column, DateTime
from datetime import datetime

from api.core.utils.generic_models import QuestionDifficultyEnum, QuestionTypeEnum



class MCQOptionBase(SQLModel):
    option_text: str = Field(default=None, max_length=500)
    is_correct: bool = Field(default=False)

    question_id: int | None = Field(
        foreign_key='questionbank.id', default=None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "option_text": "The use of interfaces to type-check an object's structure.",
                "is_correct": True,
                "question_id": 1
            }
        }

class MCQOption(MCQOptionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
            DateTime(timezone=True),
            onupdate=datetime.utcnow,
            nullable=False,
        ))

    # question Relationship
    question: "QuestionBank" = Relationship(back_populates='options') # type: ignore

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


class QuestionBankBase(SQLModel):
    question_text: str
    is_verified: bool = False
    points: int = Field(default=0)
    difficulty: QuestionDifficultyEnum = QuestionDifficultyEnum.easy
    topic_id: int = Field(foreign_key='topic.id')
    question_type: QuestionTypeEnum = Field(default=QuestionTypeEnum.single_select_mcq)

    class Config:
        json_schema_extra = {
            "example": {
                "question_text": "What is a common cause of syntax errors in TypeScript?",
                "is_verified": True,
                "points": 1,
                "difficulty": "easy",
                "topic_id": 1,
                "question_type": "single_select_mcq",
                    }
                }

class QuestionBank(QuestionBankBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # topic Relationship
    topic: 'api.quiz.topic.models.Topic' = Relationship(
        back_populates='questions')

    # MCQ Options Relationship
    options: list['MCQOption'] = Relationship(back_populates='question')

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
            DateTime(timezone=True),
            onupdate=datetime.utcnow,
            nullable=False,
        ))

class QuestionBankCreate(QuestionBankBase):
    # pass
    options: list["MCQOptionCreate"] = [] 

    class Config:
        json_schema_extra = {
            "example": {
                "question_text": "What is a common cause of syntax errors in TypeScript?",
                "is_verified": True,
                "points": 1,
                "difficulty": "easy",
                "topic_id": 1,
                "question_type": "single_select_mcq",
                "options": [
                    { "is_correct": True, "option_text": "Missing semicolons at the end of statements" },
                    { "is_correct": False, "option_text": "Missing types in function parameters" }
                ]
            }
        }

class QuestionBankRead(QuestionBankBase):
    id: int
    created_at: datetime
    updated_at: datetime


    class Config:
        json_schema_extra = {
            "example": {
                "question_text": "What is a common cause of syntax errors in TypeScript?",
                "is_verified": True,
                "points": 1,
                "difficulty": "easy",
                "topic_id": 1,
                "question_type": "single_select_mcq",
                "options": [
                    { "is_correct": True, "option_text": "Missing semicolons at the end of statements" },
                    { "is_correct": False, "option_text": "Missing types in function parameters" }
                ]
            }
        }

class QuestionBankUpdate(QuestionBankBase):
    question_text: str | None = None
    is_verified: bool | None = None
    points: int | None = None
    difficulty: QuestionDifficultyEnum | None = None
    topic_id: int | None = None
    question_type: QuestionTypeEnum | None = None


class QuestionBankReadWithOptions(QuestionBankRead):
    options: list['MCQOptionRead'] = []