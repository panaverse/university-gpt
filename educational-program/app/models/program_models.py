from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from app.models.base import BaseIdModel

if TYPE_CHECKING:
    from app.models.university_models import University
    from app.models.course_models import Course

example_input_prog = {
    "university_id": 1,
    "name": "Artificial Intelligence",
    "description": "The program of Artificial Intelligence is a leading educational program in Pakistan.",
}

example_output_prog = {
    "id": 1,
    "university_id": 1,
    "name": "Artificial Intelligence",
    "description": "The program of Artificial Intelligence is a leading educational program in Pakistan.",
}


# Model for ProgramBase with common fields
class ProgramBase(SQLModel):
    name: str
    description: str | None = None


# Model for creating a Program in the database
class Program(BaseIdModel, ProgramBase, table=True):
    # Foreign Key to University
    university_id: int | None = Field(default=None, foreign_key="university.id")
    # 1. Relationship with University
    university: "University" = Relationship(back_populates="programs")
    # 2. Relationship with Course
    courses: list["Course"] = Relationship(back_populates="program")


# Model for reading a Program from the database this will be send as response back to the client
class ProgramRead(ProgramBase):
    id: int
    university_id: int | None

    class ConfigDict:
        json_schema_extra = {"example": example_output_prog}


# Model for creating a Program this will be to get data from the client
class ProgramCreate(ProgramBase):
    university_id: int

    class ConfigDict:
        json_schema_extra = {"example": example_input_prog}


# Model for updating a Program this will be to get data from the client
class ProgramUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    university_id: int | None = None

    class ConfigDict:
        json_schema_extra = {"example": example_input_prog}