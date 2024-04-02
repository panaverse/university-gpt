from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

from app.models.base import BaseIdModel

if TYPE_CHECKING:
    from app.models.topic_models import Topic  # Avoid circular imports at runtime
    from app.models.quiz_models import Quiz
# ------------------------------------------------
# University Model
# ------------------------------------------------
# Response Model examples
example_input_uni = {
    "university_name": "University of PIAIC",
    "university_desc": "The University of PIAIC is a leading educational institution in Pakistan.",
}

example_output_uni = {
    "id": 1,
    "university_name": "University of PIAIC",
    "university_desc": "The University of PIAIC is a leading educational institution in Pakistan.",
    # "created_at": "2021-07-10T14:48:00.000Z",
    # "updated_at": "2021-07-10T14:48:00.000Z",
}


# Model for UniversityBase with common fields
class UniversityBase(SQLModel):
    """
    Fields:
    university_name (required): str: Name of the University
    university_desc (optional): str: Description of the University
    """

    university_name: str
    university_desc: str | None = None


# Model for creating a University in the database
class University(BaseIdModel, UniversityBase, table=True):
    """
    Fields:
    university_name, university_desc (required): inherited from UniversityBase
    """

    # 1. Relationship with Program
    programs: list["Program"] = Relationship(back_populates="university")


# Model for reading a University from the database
# this will be send as response back to the client
class UniversityRead(UniversityBase):
    """
    Fields:
    university_name, university_desc (required): inherited from UniversityBase
    id: int (required): ID of the University
    created_at: datetime (required): Date and time when the University was created
    updated_at: datetime (required): Date and time when the University was last updated
    """

    id: int

    class Config:
        json_schema_extra = {"example": example_output_uni}


# Model for creating a University
# this will be to get data from the client
class UniversityCreate(UniversityBase):
    """
    Fields:
    university_name (required): str: Name of the University
    university_desc (optional): str: Description of the University
    """

    class Config:
        json_schema_extra = {"example": example_input_uni}


# Model for updating a University
# this will be to get data from the client
class UniversityUpdate(SQLModel):
    """
    Fields:
    university_name (optional): str: Name of the University
    university_desc (optional): str: Description of the University
    """

    university_name: str | None = None
    university_desc: str | None = None

    class Config:
        json_schema_extra = {"example": example_input_uni}


# ------------------------------------------------
# Program Model
# ------------------------------------------------

example_input_prog = {
    "university_id": 1,
    "program_name": "Artificial Intelligence",
    "program_desc": "The program of Artificial Intelligence is a leading educational program in Pakistan.",
}

example_output_prog = {
    "id": 1,
    "university_id": 1,
    "program_name": "Artificial Intelligence",
    "program_desc": "The program of Artificial Intelligence is a leading educational program in Pakistan.",
    # "created_at": "2021-07-10T14:48:00.000Z",
    # "updated_at": "2021-07-10T14:48:00.000Z",
}


# Model for ProgramBase with common fields
class ProgramBase(SQLModel):
    """
    Fields:
    program_name (required): str: Name of the Program
    program_desc (optional): str: Description of the Program
    """

    program_name: str
    program_desc: str | None = None


# Model for creating a Program in the database
class Program(BaseIdModel, ProgramBase, table=True):
    """
    Fields:
    program_name, program_desc (required): inherited from ProgramBase
    id: int (required): ID of the Program
    university_id: int (required): ID of the University
    created_at: datetime (required): Date and time when the Program was created
    updated_at: datetime (required): Date and time when the Program was last updated
    """

    # Foreign Key to University
    university_id: int | None = Field(default=None, foreign_key="university.id")

    # 1. Relationship with University
    university: "University" = Relationship(back_populates="programs")
    # 2. Relationship with Course
    courses: list["Course"] = Relationship(back_populates="program")


# Model for reading a Program from the database
# this will be send as response back to the client
class ProgramRead(ProgramBase):
    """
    Fields:
    program_name, program_desc (required): inherited from ProgramBase
    id: int (required): ID of the Program
    university_id: int (required): ID of the University
    created_at: datetime (required): Date and time when the Program was created
    updated_at: datetime (required): Date and time when the Program was last updated
    """

    id: int
    university_id: int | None

    class Config:
        json_schema_extra = {"example": example_output_prog}


# Model for creating a Program
# this will be to get data from the client
class ProgramCreate(ProgramBase):
    """
    Fields:
    program_name (required): str: Name of the Program
    program_desc (optional): str: Description of the Program
    university_id (required): int: ID of the University
    """

    university_id: int

    class Config:
        json_schema_extra = {"example": example_input_prog}


# Model for updating a Program
# this will be to get data from the client
class ProgramUpdate(SQLModel):
    """
    Fields:
    program_name (optional): str: Name of the Program
    program_desc (optional): str: Description of the Program
    """

    program_name: str | None = None
    program_desc: str | None = None
    university_id: int | None = None

    class Config:
        json_schema_extra = {"example": example_input_prog}


# ------------------------------------------------
# Course Model
# ------------------------------------------------

example_input_course = {
    "program_id": 1,
    "course_name": "Python Programming",
    "course_desc": "The course of Python Programming is a leading educational course in Pakistan.",
}

example_output_course = {
    "id": 1,
    "program_id": 1,
    "course_name": "Python Programming",
    "course_desc": "The course of Python Programming is a leading educational course in Pakistan.",
    # "created_at": "2021-07-10T14:48:00.000Z",
    # "updated_at": "2021-07-10T14:48:00.000Z",
}


# Model for CourseBase with common fields
class CourseBase(SQLModel):
    """
    Fields:
    course_name (required): str: Name of the Course
    course_desc (optional): str: Description of the Course
    """

    course_name: str
    course_desc: str | None = None


# Model for creating a Course in the database
class Course(BaseIdModel, CourseBase, table=True):
    """
    Fields:
    course_name, course_desc (required): inherited from CourseBase
    id: int (required): ID of the Course
    program_id: int (required): ID of the Program
    created_at: datetime (required): Date and time when the Course was created
    updated_at: datetime (required): Date and time when the Course was last updated
    """

    # Foreign Key to Program
    program_id: int = Field(default=None, foreign_key="program.id")

    # 1. Relationship with Program
    program: "Program" = Relationship(back_populates="courses")
    # 2. Relationship with Topic
    topics: list["Topic"] = Relationship(back_populates="course")
    #  3. Relationship to Quiz
    quizzes: list["Quiz"] = Relationship(back_populates="course")


# Model for reading a Course from the database
# this will be send as response back to the client
class CourseRead(CourseBase):
    """
    Fields:
    course_name, course_desc (required): inherited from CourseBase
    id: int (required): ID of the Course
    program_id: int (required): ID of the Program
    created_at: datetime (required): Date and time when the Course was created
    updated_at: datetime (required): Date and time when the Course was last updated
    """

    id: int
    program_id: int | None

    class Config:
        json_schema_extra = {"example": example_output_course}


# Model for creating a Course
# this will be to get data from the client
class CourseCreate(CourseBase):
    """
    Fields:
    course_name (required): str: Name of the Course
    course_desc (optional): str: Description of the Course
    program_id (required): int: ID of the Program
    """

    program_id: int

    class Config:
        json_schema_extra = {"example": example_input_course}


# Model for updating a Course
# this will be to get data from the client
class CourseUpdate(SQLModel):
    """
    Fields:
        course_name (optional): str: Name of the Course
        course_desc (optional): str: Description of the Course
    """

    course_name: str | None = None
    course_desc: str | None = None
    program_id: int | None = None

    class Config:
        json_schema_extra = {"example": example_input_course}
