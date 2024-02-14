from sqlmodel import Field, Relationship, SQLModel, Column, DateTime
from datetime import datetime

class ResultBase(SQLModel):
    answer_sheet_id: int = Field(foreign_key="quiz.id")
    student_id: int = Field(foreign_key="student.student_id")
    quiz_id: int = Field(foreign_key="quiz.id")

    # def calcaulte_percentage(self):
    #     return self.obtained_marks/self.total_marks * 100

    class Config:
        json_schema_extra = {
            "example": {
                "answer_sheet_id": 1,
                "student_id": 1,
                "quiz_id": 1
            }
        }
 

class Result(ResultBase, table=True): 
    id : int = Field(default=None, primary_key=True)
    total_marks: int
    obtained_marks: int

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
        DateTime(timezone=True),
        onupdate=datetime.utcnow,
        nullable=False,
    ))

class ResultCreate(ResultBase):
    pass

class ResultRead(ResultBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ResultUpdate(ResultBase):
    answer_sheet_id: int | None = None
    student_id: int | None = None
    quiz_id: int | None = None
    total_marks: int | None = None
    obtained_marks: int | None = None

