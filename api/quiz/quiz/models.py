from sqlmodel import Field, SQLModel, Relationship,Column,DateTime
from datetime import timedelta
from datetime import datetime

from api.quiz.topic.models import TopicResponseWithQuestions

class QuizTopicBase(SQLModel):
    title: str
    description: str

    quiz_id: int | None = Field(foreign_key="quiz.id", default=None, index=True)
    topic_id: int = Field(foreign_key="topic.id")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "TypeScript Basics",
                "description": "This quiz is about the basics of TypeScript",
                "quiz_id": "1",
                "topic_id": "1"
            }
        }

class QuizTopic(QuizTopicBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), onupdate=datetime.utcnow, nullable=False))
    
    # Quiz Relationship
    quiz: 'Quiz' = Relationship(back_populates="quiz_topics")

    # Topic Relationship
    topic: 'api.quiz.topic.models.Topic' = Relationship(back_populates="quiz_topics")

    quiz_question_instances: list['QuizQuestionInstances'] = Relationship(back_populates="quiz_topic", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class QuizTopicCreate(QuizTopicBase):
    pass

class QuizTopicRead(QuizTopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

class QuizTopicUpdate(QuizTopicBase):
    title: str | None = None
    description: str | None = None
    quiz_id: int | None = None
    topic_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


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
    id: int | None = Field(default=None, primary_key=True, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), onupdate=datetime.utcnow, nullable=False))

    quiz_topics: list['QuizTopic'] = Relationship(back_populates="quiz", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    quiz_question_instances: list['QuizQuestionInstances'] = Relationship(back_populates="quiz", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class QuizCreate(QuizBase):
    # pass
    quiz_topics: list['QuizTopicCreate'] = []

    class Config:
        json_schema_extra = {
            "example": {
                "title": "OOPs Paradigm in Typescript",
                "duration": 30,
                "quiz_topics": [
                    {"title": "TypeScript Basics", "description": "This quiz is about the basics of TypeScript", "topic_id": "1"}
                    ]
                }
            }

class QuizRead(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime

class QuizUpdate(QuizBase):
    title: str | None = None
    duration: timedelta | None = None
    quiz_topics: list['QuizTopicCreate'] = []

    class Config:
        json_schema_extra = {
            "example": {
                "title": "OOPs Paradigm in Typescript",
                "duration": 30,
                "quiz_topics": [
                    {"title": "TypeScript Basics", "description": "This quiz is about the basics of TypeScript", "topic_id": "1"}
                    ]
                }
            }

class QuizReadWithQuizTopics(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # TODO: Review Again
    quiz_topics: list[QuizTopicRead] = []

class QuizTopicsReadWithTopic(QuizTopicRead):

    topic: TopicResponseWithQuestions | None = None

# Table for QuizQuestions
class QuizQuestionInstancesBase(SQLModel):
    quiz_id: int = Field(foreign_key="quiz.id", index=True)
    quiz_topic_id: int = Field(foreign_key="quiztopic.id", index=True)
    question_id: int = Field(foreign_key="questionbank.id", index=True)
    is_muted: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": 1,
                "question_id": 1,
                "quiz_topic_id": 1,
            }
        }

class QuizQuestionInstances(QuizQuestionInstancesBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), onupdate=datetime.utcnow, nullable=False))

    # Quiz Relationship
    quiz: 'Quiz' = Relationship(back_populates="quiz_question_instances")

    # Quiz Topic Relationship
    quiz_topic: 'QuizTopic' = Relationship(back_populates="quiz_question_instances")

    # Question Relationship
    question: 'api.quiz.question.models.QuestionBank' = Relationship(back_populates="quiz_question_instances")

class QuizQuestionInstancesCreate(QuizQuestionInstancesBase):
    pass

class QuizQuestionInstancesRead(QuizQuestionInstancesBase):
    id: int
    created_at: datetime
    updated_at: datetime

class QuizQuestionInstancesUpdate(QuizQuestionInstancesBase):
    quiz_id: int | None = None
    quiz_topic_id: int | None = None
    question_id: int | None = None
    is_muted: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class QuizQuestionInstancesReadWithQuestion(QuizQuestionInstancesRead):
    question: 'api.quiz.question.models.QuestionBankRead' = []

