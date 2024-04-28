from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

from app.models.base import BaseIdModel, QuizDifficultyEnum
from app.models.topic_models import Topic
from app.models.link_models import QuizTopic
from app.models.question_models import QuestionBankRead

if TYPE_CHECKING:
    from app.models.question_models import QuestionBank
    from app.models.quiz_setting import QuizSetting


# -------------------------------------------
# Quiz Models
# -------------------------------------------
# Response model
example_quiz_input = {
    "quiz_title": "TypeScript Quiz",
    "difficulty_level": "easy",
    "random_flag": True,
    "course_id": 1,
}

example_quiz_input_create = {
    "quiz_title": "TypeScript Quiz",
    "difficulty_level": "easy",
    "random_flag": True,
    "course_id": 1,
    "add_topic_ids": [1],
}

example_quiz_input_update = {
    "quiz_title": "TypeScript Quiz",
    "difficulty_level": "easy",
    "random_flag": True,
    "course_id": 1,
    "add_topic_ids": [1, 2, 3],
    "remove_topic_ids": [4],
}

example_quiz_output = {
    "quiz_title": "TypeScript Quiz",
    "difficulty_level": "easy",
    "random_flag": True,
    "course_id": 1,
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z",
}


class QuizBase(SQLModel):
    quiz_title: str = Field(max_length=160, index=True)
    difficulty_level: QuizDifficultyEnum = Field(
        default=QuizDifficultyEnum.easy
    )
    random_flag: bool = Field(default=False)
    total_points: int | None = Field(default=0)
    course_id: int | None = Field(index=True, default=None)

    class Config:
        json_schema_extra = {"example": example_quiz_input}


class Quiz(BaseIdModel, QuizBase, table=True):
    topics: list["Topic"] = Relationship(back_populates="quizzes", link_model=QuizTopic)

    # course: "Course" = Relationship(back_populates="quizzes")

    quiz_questions: list["QuizQuestion"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    quiz_settings: list["QuizSetting"] = Relationship(
        back_populates="quiz",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"},
    )

    # answer_sheets: list["AnswerSheet"] = Relationship(back_populates="quiz")


class QuizCreate(QuizBase):
    # topic ids to fetch and add existing topics to the quiz
    add_topic_ids: list[int] = []

    class Config:
        json_schema_extra = {"example": example_quiz_input_create}


class QuizRead(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime


class QuizReadWithTopics(QuizRead):
    topics: list["Topic"] = []


class QuizUpdate(SQLModel):
    quiz_title: str | None = None
    difficulty_level: QuizDifficultyEnum | None = None
    random_flag: bool | None = None
    total_points: int | None = None
    course_id: int | None = None

    add_topic_ids: list[int] = []
    remove_topic_ids: list[int] = []

    class Config:
        json_schema_extra = {"example": example_quiz_input_update}



# -------------------------------------------
# QuizQuestion Models
# -------------------------------------------

example_quiz_question_input = {"quiz_id": 1, "question_id": 1, "topic_id": 1}


class QuizQuestionBase(SQLModel):
    quiz_id: int | None = Field(
        foreign_key="quiz.id", index=True, primary_key=True, default=None
    )
    question_id: int | None = Field(
        foreign_key="questionbank.id", index=True, primary_key=True, default=None
    )
    topic_id: int = Field(
        foreign_key="topic.id", index=True, primary_key=True, default=None
    )

    class Config:
        json_schema_extra = {"example": example_quiz_question_input}


class QuizQuestion(QuizQuestionBase, table=True):
    # RelationShips
    quiz: "Quiz" = Relationship(back_populates="quiz_questions")
    topic: "Topic" = Relationship(back_populates="quiz_questions")
    question: "QuestionBank" = Relationship(back_populates="quiz_questions")


class QuizQuestionRead(QuizQuestionBase):
    pass


class QuizQuestionReadQuestionBank(QuizQuestionBase):
    question: QuestionBankRead


class QuizReadWithQuestionsAndTopics(QuizReadWithTopics):
    quiz_questions: list["QuizQuestionReadQuestionBank"] = []

