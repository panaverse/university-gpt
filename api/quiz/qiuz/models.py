from sqlmodel import Field, SQLModel, Relationship,Column,DateTime
from datetime import timedelta
from datetime import datetime

class QuizTopicBase(SQLModel):
    quiz_topic_title: str
    quiz_topic_description: str

    class Config:
        json_schema_extra = {
            "example": {
                "quiz_topic_title": "TypeScript Basics",
                "quiz_topic_description": "This quiz is about the basics of TypeScript"
            }
        }


class QuizTopic(QuizTopicBase, table=True):
    id: int = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quiz.id")
    quiz: 'Quiz' = Relationship(back_populates="quiz_topic")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
            DateTime(timezone=True),
            onupdate=datetime.utcnow,
            nullable=False,
        ))



class QuizBase(SQLModel):
    title: str
    duration: timedelta = Field(default=timedelta(minutes=0))

    class Config:
        json_schema_extra = {
            "example": {
                "title": "TypeScript",
                "duration": 30
            }
        }
   


class Quiz(QuizBase, table=True):
    id: int = Field(default=None, primary_key=True)
    quiz_topic: list['QuizTopic'] = Relationship(back_populates="quiz")


    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
            DateTime(timezone=True),
            onupdate=datetime.utcnow,
            nullable=False,
        ))


class QuizCreate(QuizBase):
    pass

class QuizRead(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime

class QuizUpdate(QuizBase):
    title: str | None = None
    duration: timedelta | None = None
    quiz_topic: list[QuizTopic] | None = None

class QuizTopicCreate(QuizTopicBase):
    pass

class QuizTopicRead(QuizTopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

class QuizTopicUpdate(QuizTopicBase):
    quiz_topic_title: str | None = None
    quiz_topic_description: str | None = None
    quiz_id: int | None = None
    quiz: Quiz | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None