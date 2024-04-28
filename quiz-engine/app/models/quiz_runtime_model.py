
from sqlmodel import Field, SQLModel, Relationship
from pydantic import validator
from datetime import datetime, timedelta

from app.models.base import QuestionTypeEnum

import random

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
    question_type: QuestionTypeEnum = Field(default=QuestionTypeEnum.single_select_mcq)
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

    # Custom validator to shuffle the order of quiz_questions
    @validator("quiz_questions", pre=True)
    def shuffle_quiz_questions(cls, v):
        random.shuffle(v)
        return v

    # Custom validator to directly include question data

    @validator("quiz_questions", pre=True, each_item=True)
    def unpack_question_data(cls, v):
        # Assuming 'v' is an instance of QuizQuestionFormating or similar
        # Adjust this logic based on the actual structure of your data
        return v.question if hasattr(v, "question") else v

class WrapperRuntimeQuiz(SQLModel):
    total_points: int
    quiz_title: str
    course_id: int
    quiz_questions: list[QuestionRuntimeQuiz] = []

    # Custom validator to shuffle the order of quiz_questions
    @validator("quiz_questions", pre=True)
    def shuffle_quiz_questions(cls, v):
        random.shuffle(v)
        return v

    # Custom validator to directly include question data

    @validator("quiz_questions", pre=True, each_item=True)
    def unpack_question_data(cls, v):
        # Assuming 'v' is an instance of QuizQuestionFormating or similar
        # Adjust this logic based on the actual structure of your data
        return v.question if hasattr(v, "question") else v
