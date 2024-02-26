from sqlmodel import Field, SQLModel, Relationship, DateTime, Column
from datetime import datetime


class AnswerSheetBase(SQLModel):
    quiz_id: int = Field(foreign_key="quiz.id")
    student_id: int = Field(foreign_key="student.student_id")
    answerJSON: str | None
    quiz_start_time: datetime
    quiz_end_time: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": 1,
                "student_id": 1,
                "quiz_start_time": 1625850000,
                "quiz_end_time": 1625850000
            }
        }


class AnswerSheet(AnswerSheetBase, table=True):
    id: int = Field(default=None, primary_key=True)
    student: 'app.quiz.user.models.Student' = Relationship(
        back_populates="answersheets")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
        DateTime(timezone=True),
        onupdate=datetime.utcnow,
        nullable=False,
    ))


class AnswerSheetCreate(AnswerSheetBase):
    pass


class AnswerSheetRead(AnswerSheetBase):
    id: int
    created_at: datetime
    updated_at: datetime


class AnswerSheetUpdate(AnswerSheetBase):
    quiz_id: int | None = None
    student_id: int | None = None
    quiz_start_time: datetime | None = None
    quiz_end_time: datetime | None = None
    answerJSON: str | None = None
