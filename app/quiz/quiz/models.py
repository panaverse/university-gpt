from sqlmodel import Field, SQLModel, Relationship
from pydantic import validator
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from app.core.utils.generic_models import QuestionTypeEnum, BaseIdModel, QuestionDifficultyEnum
from app.quiz.quiz.link_models import QuizTopic
from app.quiz.question.models import QuestionBankRead
from app.quiz.topic.models import Topic, TopicBase
from app.quiz.answersheet.models import AnswerSheetRead

if TYPE_CHECKING:
    from app.quiz.question.models import QuestionBank
    from app.quiz.university.models import Course
    from app.quiz.answersheet.models import AnswerSheet

# -------------------------------------------
    # Quiz Models
# -------------------------------------------
# Response model
example_quiz_input = {
    "quiz_title": "TypeScript Quiz",
    "difficulty_level": "easy",
    "random_flag": True,
    "course_id": 1
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
    "remove_topic_ids": [4]
}

example_quiz_output = {
    "quiz_title": "TypeScript Quiz",
    "difficulty_level": "easy",
    "random_flag": True,
    "course_id": 1,
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z"
}


class QuizBase(SQLModel):
    quiz_title: str = Field(max_length=160, index=True)
    difficulty_level: QuestionDifficultyEnum = Field(
        default=QuestionDifficultyEnum.easy)
    random_flag: bool = Field(default=False)
    total_points: int | None = Field(default=0)
    course_id: int | None = Field(foreign_key="course.id", default=None)

    class Config:
        json_schema_extra = {
            "example": example_quiz_input
        }


class Quiz(BaseIdModel, QuizBase, table=True):

    topics: list['Topic'] = Relationship(
        back_populates="quizzes", link_model=QuizTopic)

    course: 'Course' = Relationship(back_populates="quizzes")

    quiz_questions: list['QuizQuestion'] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    quiz_settings: list['QuizSetting'] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})

    answer_sheets: list['AnswerSheet'] = Relationship(back_populates="quiz")


class QuizCreate(QuizBase):
    # topic ids to fetch and add existing topics to the quiz
    add_topic_ids: list[int] = []

    class Config:
        json_schema_extra = {
            "example": example_quiz_input_create
        }


class QuizRead(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime


class QuizReadWithTopics(QuizRead):
    topics: list['Topic'] = []


class QuizUpdate(QuizBase):
    quiz_title: str | None = None
    difficulty_level: QuestionDifficultyEnum | None = None
    random_flag: bool | None = None
    total_points: int | None = None
    course_id: int | None = None

    add_topic_ids: list[int] = []
    remove_topic_ids: list[int] = []

    class Config:
        json_schema_extra = {
            "example": example_quiz_input_update
        }


# -------------------------------------------
        # QuizSetting Models
# -------------------------------------------
# Response model
example_quiz_setting_input = {
    "quiz_id": 1,
    "instructions": "Read the questions carefully.",
    "time_limit": "P3D",
    "start_time": "2023-02-26T14:56:46.277Z",
    "end_time": "2025-02-26T14:56:46.277Z",
    "quiz_key": "BAT_Q1TS278"
}

example_quiz_setting_output = {
    "quiz_id": 1,
    "instructions": "Read the questions carefully.",
    "time_limit": "P3D",
    "start_time": "2021-07-10T14:48:00.000Z",
    "end_time": "2021-07-10T14:48:00.000Z",
    "quiz_key": "BAT_Q1TS278",
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z"
}

# Model for QuizSettingsBase with common fields


class QuizSettingBase(SQLModel):
    quiz_id: int = Field(foreign_key="quiz.id")
    instructions: str = Field(default=None)
    time_limit: timedelta = Field()
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    quiz_key: str = Field(max_length=160)

# Model for creating a QuizSettings in the database


class QuizSetting(BaseIdModel, QuizSettingBase, table=True):
    # 1. Relationship with Quiz
    quiz: Quiz = Relationship(back_populates="quiz_settings", sa_relationship_kwargs={"lazy": "joined"})

# Model for creating a QuizSetting


class QuizSettingCreate(QuizSettingBase):
    pass
        

class QuizSettingRead(QuizSettingBase):
    id: int
    class Config:
        json_schema_extra = {
            "example": example_quiz_setting_output
        }

# Model for updating a QuizSetting in the database


class QuizSettingUpdate(SQLModel):
    quiz_id: int | None = None
    instructions: str | None = None
    time_limit: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    quiz_key: str | None = None

    class Config:
        json_schema_extra = {
            "example": example_quiz_setting_input
        }


# -------------------------------------------
        # QuizQuestion Models
# -------------------------------------------

example_quiz_question_input = {
    "quiz_id": 1,
    "question_id": 1,
    "topic_id": 1
}


class QuizQuestionBase(SQLModel):
    quiz_id: int | None = Field(
        foreign_key="quiz.id", index=True, primary_key=True, default=None)
    question_id: int | None = Field(
        foreign_key="questionbank.id", index=True, primary_key=True, default=None)
    topic_id: int = Field(
        foreign_key="topic.id", index=True, primary_key=True, default=None)

    class Config:
        json_schema_extra = {
            "example": example_quiz_question_input
        }


class QuizQuestion(QuizQuestionBase, table=True):

    # RelationShips
    quiz: 'Quiz' = Relationship(back_populates="quiz_questions")
    question: 'QuestionBank' = Relationship(back_populates="quiz_questions")
    topic: 'Topic' = Relationship(back_populates="quiz_questions")


class QuizQuestionRead(QuizQuestionBase):
    pass


class QuizQuestionReadQuestionBank(QuizQuestionBase):
    question: QuestionBankRead


class QuizReadWithQuestionsAndTopics(QuizReadWithTopics):
    quiz_questions: list['QuizQuestionReadQuestionBank'] = []


# TODO: Review when create quiz apis - LEAVING AS IT IS THE BELOW Models
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
    question_type: QuestionTypeEnum = Field(
        default=QuestionTypeEnum.single_select_mcq)
    options: list[MCQOptionRuntimeQuiz] = []


class RuntimeQuizGenerated(SQLModel):
    answer_sheet_id: int
    quiz_title: str
    course_id: int
    instructions: str
    quiz_questions: list[QuestionRuntimeQuiz] = []

    student_id: int 
    quiz_id: int 
    time_limit: timedelta
    time_start: datetime 
    total_points: int
    quiz_key: str 

    # Custom validator to directly include question data

    @validator('quiz_questions', pre=True, each_item=True)
    def unpack_question_data(cls, v):
        # Assuming 'v' is an instance of QuizQuestionFormating or similar
        # Adjust this logic based on the actual structure of your data
        return v.question if hasattr(v, 'question') else v
