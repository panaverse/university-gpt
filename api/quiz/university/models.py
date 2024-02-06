from  sqlmodel import SQLModel, Field, ForeignKey


# Base classes for the models
class UniversityBase(SQLModel):
    name: str
    description: str = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "PIAIC",
                "description": "Pakistan's largest AI institute"
               
            }
        }

class ProgramBase(SQLModel):
    name: str
    description: str = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "AI",
                "description": "Artificial Intelligence",
                "university_id": 1
            }
        }

class CourseBase(SQLModel):
    name: str
    description: str = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "AI",
                "description": "Artificial Intelligence",
                "program_id": 1
            }
        }

# Models for the tables
class University(UniversityBase, table=True):
    university_id: int | None = Field(default=None, primary_key=True)

class Program(ProgramBase, table=True):
    program_id: int | None = Field(default=None, primary_key=True)
    university_id: int = Field(foreign_key="university.university_id")

class Course(CourseBase, table=True):
    course_id: int | None = Field(default=None, primary_key=True)
    program_id: int = Field(foreign_key="program.program_id")


# Models for the request and response creation
class UniversityCreate(UniversityBase):
    pass

class ProgramCreate(ProgramBase):
    pass

class CourseCreate(CourseBase):
    pass

# Models for the request and response reading
class UniversityRead(UniversityBase):
    id: int
    name: str | None = None
    description: str | None = None

class ProgramRead(ProgramBase):
    id: int
    name: str | None = None
    description: str | None = None
    university_id: int | None = None

class CourseRead(CourseBase):
    id: int
    name: str | None = None
    description: str | None = None
    program_id: int | None = None


# Models for the request and response updating
class UniversityUpdate(SQLModel):
    name: str | None = None
    description: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "PIAIC",
                "description": "Pakistan's largest AI institute"
            }
        }

class ProgramUpdate(SQLModel):
    name: str | None = None
    description: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "AI",
                "description": "Artificial Intelligence",
                "university_id": 1
            }
        }

class CourseUpdate(SQLModel):
    name: str | None = None
    description: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "AI",
                "description": "Artificial Intelligence",
                "program_id": 1
            }
        }
