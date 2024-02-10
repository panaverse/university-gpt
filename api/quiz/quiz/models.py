from sqlmodel import Field, SQLModel, Relationship, Column, DateTime
from datetime import timedelta
from datetime import datetime
from api.quiz.quiz.link_models import QuizTopic
from api.quiz.topic.models import Topic, TopicBase
from api.quiz.question.models import QuestionBank, QuestionBankRead

class QuizBase(SQLModel):
    title: str = Field(max_length=160, index=True)
    description: str | None = None
    duration: timedelta = Field(default=timedelta(minutes=0))
    course_id: int | None = Field(foreign_key="course.course_id", default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "TypeScript",
                "description": "This quiz is about TypeScript",
                "duration": 30,
                "course_id": 1
            }
        }
   
class Quiz(QuizBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), onupdate=datetime.utcnow, nullable=False))

    topics: list['Topic'] = Relationship(back_populates="quizzes", link_model=QuizTopic)

    quiz_questions: list['QuizQuestion'] = Relationship(back_populates="quiz", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class QuizCreate(QuizBase):
    # topic ids to fetch and add existing topics to the quiz
    topic_ids: list[int] = []

    # Add New Topics to the Quiz
    topics: list[TopicBase] = []

    class Config:
        json_schema_extra = {
            "example": {
                "title": "TypeScript Quiz",
                "description": "This quiz is about TypeScript Basics & OOP",
                "duration": 30,
                "course_id": 1,
                "topic_ids": [1, 2, 3],
                "topics": [
                    {"title": "OPTIONALLY ADD A TOPIC", "description": "OR Add id of the existing topic in topic_ids"},
                    {"title": "OOP Paradigm:", "description": "Learn about OOP Paradigm", "parent_id": 1}
                ]
            }
        }

class QuizRead(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime

class QuizReadWithTopics(QuizRead):
    topics: list['Topic'] = []

class QuizReadWithQuestionsAndTopics(QuizReadWithTopics):
    quiz_questions: list['QuizQuestionReadQuestionBank'] = []

class QuizUpdate(QuizBase):
    title: str | None = None
    duration: timedelta | None = None
    description: str | None = None
    course_id: int | None = None

    add_topic_ids: list[int] = []

    remove_topic_ids: list[int] = []

    class Config:
        json_schema_extra = {
            "example": {
                "title": "TypeScript Quiz",
                "description": "This quiz is about TypeScript Basics & OOP",
                "duration": 30,
                "course_id": 1,
                "add_topic_ids": [1, 2, 3],
                "remove_topic_ids": [4]
                }
            }

class QuizQuestionBase(SQLModel):
    quiz_id: int | None = Field(foreign_key="quiz.id", index=True, primary_key=True, default=None)
    question_id: int | None = Field(foreign_key="questionbank.id", index=True, primary_key=True, default=None)
    is_muted: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": 1,
                "question_id": 1,
                "is_muted": "False"
            }
        }

class QuizQuestion(QuizQuestionBase, table=True):

    # RelationShips Here as we have extra fields
    quiz : 'Quiz' = Relationship(back_populates="quiz_questions")
    question : 'QuestionBank' = Relationship(back_populates="quiz_questions")

    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": 1,
                "question_id": 1,
                "is_muted": "False"
            }
        }

class QuizQuestionUpdate(SQLModel):
    is_muted: bool | None = None
    class Config:
        json_schema_extra = {
            "example": {
                "is_muted": "False"
            }
        }
class QuizQuestionRead(QuizQuestionBase):
    pass

class QuizQuestionReadQuestionBank(QuizQuestionBase):
    question: QuestionBankRead