from sqlmodel import Field, Relationship, SQLModel, Column, DateTime
from datetime import datetime

from api.core.utils.generic_models import QuestionDifficultyEnum, QuestionTypeEnum
from typing import Optional

class QuestionBankBase(SQLModel):
    question_text: str
    is_verified: bool = False
    points: int = Field(default=0)
    difficulty: QuestionDifficultyEnum = QuestionDifficultyEnum.easy
    topic_id: int = Field(foreign_key='topic.id')
    question_type: QuestionTypeEnum = Field(default=QuestionTypeEnum.single_select_mcq)


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
    pass

class QuestionBankRead(QuestionBankBase):
    id: int
    created_at: datetime
    updated_at: datetime

class QuestionBankUpdate(QuestionBankBase):
    question_text: str | None = None
    is_verified: bool | None = None
    points: int | None = None
    difficulty: QuestionDifficultyEnum | None = None
    topic_id: int | None = None
    question_type: QuestionTypeEnum | None = None


class MCQOptionBase(SQLModel):
    option_text: str = Field(default=None, max_length=500)
    is_correct: bool = False

    question_id: int = Field(
        foreign_key='questionbank.id')

class MCQOption(MCQOptionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
            DateTime(timezone=True),
            onupdate=datetime.utcnow,
            nullable=False,
        ))

    # question Relationship
    question: QuestionBank = Relationship(back_populates='options')

class MCQOptionCreate(MCQOptionBase):
    pass

class MCQOptionRead(MCQOptionBase):
    id: int
    question: QuestionBank | None = None
    created_at: datetime
    updated_at: datetime

class MCQOptionUpdate(MCQOptionBase):
    option_text: str | None = None
    is_correct: bool | None = None
    question_id: int | None = None