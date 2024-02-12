from sqlmodel import Field, SQLModel, Relationship, Column, DateTime
from datetime import timedelta
from datetime import datetime
from api.quiz.quiz.link_models import QuizTopic
from api.quiz.topic.models import Topic, TopicBase
from api.quiz.question.models import QuestionBank, QuestionBankRead
from api.core.utils.generic_models import QuestionTypeEnum
from pydantic import validator


class QuizBase(SQLModel):
    title: str = Field(max_length=160, index=True)
    description: str | None = None
    duration: timedelta = Field(default=timedelta(minutes=0))
    course_id: int | None = Field(foreign_key="course.course_id", default=None)

    start_date: datetime | None = None
    end_date: datetime | None = None
    instructions: str | None = None

    total_points: int = Field(default=0)

    quiz_key: str | None = Field(max_length=160, nullable=True)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "TypeScript",
                "description": "This quiz is about TypeScript",
                "duration": 30,
                "course_id": 1,
                "quiz_key": "TS123",
                "start_date": "2021-08-01T00:00:00",
                "end_date": "2021-08-09T23:59:59"
            }
        }


class Quiz(QuizBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
        DateTime(timezone=True), onupdate=datetime.utcnow, nullable=False))

    topics: list['Topic'] = Relationship(
        back_populates="quizzes", link_model=QuizTopic)

    course: 'api.quiz.university.models.Course' = Relationship(
        back_populates="quizzes")

    quiz_questions: list['QuizQuestion'] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


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
                 "quiz_key": "TS123",
                "start_date": "2021-08-01T00:00:00",
                "end_date": "2021-08-09T23:59:59",
                "instructions": "Read the instructions carefully before starting the quiz.",
                "topic_ids": [1, 2, 3],
                "topics": [
                    {"title": "OPTIONALLY ADD A TOPIC",
                        "description": "OR Add id of the existing topic in topic_ids"},
                    {"title": "OOP Paradigm:",
                        "description": "Learn about OOP Paradigm", "parent_id": 1}
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
    start_date: datetime | None = None
    end_date: datetime | None = None
    instructions: str | None = None
    total_points: int | None = None
    quiz_key: str | None = None

    add_topic_ids: list[int] = []

    remove_topic_ids: list[int] = []

    class Config:
        json_schema_extra = {
            "example": {
                "title": "TypeScript Quiz",
                "description": "This quiz is about TypeScript Basics & OOP",
                "duration": 30,
                "course_id": 1,
                "start_date": "2021-08-01T00:00:00",
                "end_date": "2021-08-09T23:59:59",
                "instructions": "Read the instructions carefully before starting the quiz.",
                "add_topic_ids": [1, 2, 3],
                "remove_topic_ids": [4]
            }
        }


class QuizQuestionBase(SQLModel):
    quiz_id: int | None = Field(
        foreign_key="quiz.id", index=True, primary_key=True, default=None)
    question_id: int | None = Field(
        foreign_key="questionbank.id", index=True, primary_key=True, default=None)
    instructor_comment: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": 1,
                "question_id": 1,
                "instructor_comment": "Defaults to None"
            }
        }


class QuizQuestion(QuizQuestionBase, table=True):

    # RelationShips Here as we have extra fields
    quiz: 'Quiz' = Relationship(back_populates="quiz_questions")
    question: 'QuestionBank' = Relationship(back_populates="quiz_questions")

    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": 1,
                "question_id": 1,
                "instructor_comment": "Defaults to None"
            }
        }


class QuizQuestionUpdate(SQLModel):
    instructor_comment: str | None = None
    class Config:
        json_schema_extra = {
            "example": {
                "instructor_comment": "This Question tests the student understanding about OOP"
            }
        }


class QuizQuestionRead(QuizQuestionBase):
    pass


class QuizQuestionReadQuestionBank(QuizQuestionBase):
    question: QuestionBankRead

# ----------------------------
# ----- Runtime Quiz Models for Validation & Serialization
# ----------------------------


class MCQOptionRuntimeQuiz(SQLModel):
    id: int
    option_text: str

class QuestionRuntimeQuiz(SQLModel):
    id: int 
    question_text: str
    points: int
    question_type: QuestionTypeEnum = Field(default=QuestionTypeEnum.single_select_mcq)
    options: list[MCQOptionRuntimeQuiz] = []

class RuntimeQuizGenerated(SQLModel):
    id: int
    title: str
    description: str
    duration: timedelta
    course_id: int
    instructions: str
    total_points: int
    quiz_key: str
    quiz_questions: list[QuestionRuntimeQuiz] = []

    # Custom validator to directly include question data
    @validator('quiz_questions', pre=True, each_item=True)
    def unpack_question_data(cls, v):
        # Assuming 'v' is an instance of QuizQuestionFormating or similar
        # Adjust this logic based on the actual structure of your data
        return v.question if hasattr(v, 'question') else v