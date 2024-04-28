from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Union
from app.models.base import BaseIdModel

if TYPE_CHECKING:
    from app.models.program_models import Program

example_input_course = {
    "program_id": 1,
    "name": "Python Programming",
    "description": "The course of Python Programming is a leading educational course in Pakistan."
}

example_output_course = {
    "id": 1,
    "program_id": 1,
    "name": "Python Programming",
    "description": "The course of Python Programming is a leading educational course in Pakistan."
}


# Model for CourseBase with common fields
class CourseBase(SQLModel):
    name: str
    description: str | None = None


# Model for creating a Course in the database
class Course(BaseIdModel, CourseBase, table=True):

    # Foreign Key to Program
    program_id: int = Field(default=None, foreign_key="program.id")

    # 1. Relationship with Program
    program: "Program" = Relationship(back_populates="courses")
    
    # TODO: Check Relationship with Topic and Quiz
    # 2. Relationship with Topic
    # topics: list["Topic"] = Relationship(back_populates="course")
    # #  3. Relationship to Quiz
    # quizzes: list["Quiz"] = Relationship(back_populates="course")


# Model for reading a Course from the database this will be send as response back to the client
class CourseRead(CourseBase):
    id: int
    program_id: int | None

    class ConfigDict:
        json_schema_extra = {"example": example_output_course}


# Model for creating a Course this will be to get data from the client
class CourseCreate(CourseBase):
    program_id: int

    class ConfigDict:
        json_schema_extra = {"example": example_input_course}


# Model for updating a Course this will be to get data from the client
class CourseUpdate(SQLModel):

    name: str | None = None
    description: str | None = None
    program_id: int | None = None

    class ConfigDict:
        json_schema_extra = {"example": example_input_course}


class PaginatedCourseRead(SQLModel):
    """
    Represents a paginated list of Course items.
    """
    count: int
    next:  Union[str, None] = None
    previous:  Union[str, None] = None
    all_records: list[CourseRead]
