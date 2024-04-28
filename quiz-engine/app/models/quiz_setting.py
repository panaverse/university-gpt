from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timedelta
from app.models.base import BaseIdModel
from app.models.quiz_models import Quiz


# Response model
example_quiz_setting_input = {
    "quiz_id": 1,
    "instructions": "Read the questions carefully.",
    "time_limit": "P3D",
    "start_time": "2023-02-26T14:56:46.277Z",
    "end_time": "2025-02-26T14:56:46.277Z",
    "quiz_key": "BAT_Q1TS278",
}

example_quiz_setting_output = {
    "quiz_id": 1,
    "instructions": "Read the questions carefully.",
    "time_limit": "P3D",
    "start_time": "2021-07-10T14:48:00.000Z",
    "end_time": "2021-07-10T14:48:00.000Z",
    "quiz_key": "BAT_Q1TS278",
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z",
}

class QuizSettingBase(SQLModel):
    quiz_id: int = Field(foreign_key="quiz.id")
    instructions: str = Field(default=None)
    time_limit: timedelta = Field()
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    quiz_key: str = Field(max_length=160)


class QuizSetting(BaseIdModel, QuizSettingBase, table=True):
    # 1. Relationship with Quiz
    quiz: Quiz = Relationship(
        back_populates="quiz_settings", sa_relationship_kwargs={"lazy": "joined"}
    )


class QuizSettingCreate(QuizSettingBase):
    pass


class QuizSettingRead(QuizSettingBase):
    id: int

    class Config:
        json_schema_extra = {"example": example_quiz_setting_output}


class QuizSettingUpdate(SQLModel):
    quiz_id: int | None = None
    instructions: str | None = None
    time_limit: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    quiz_key: str | None = None

    class Config:
        json_schema_extra = {"example": example_quiz_setting_input}