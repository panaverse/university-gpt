from sqlmodel import Field, Relationship, SQLModel

class University(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str

    programs: list["Program"] = Relationship(back_populates="university", sa_relationship_kwargs={"cascade": "delete"})

class Program(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str

    # Foreign Key & Many to one Relationship with University
    university_id: int = Field(foreign_key="university.id")
    university: University = Relationship(back_populates="programs")

    courses: list["Course"] = Relationship(back_populates="program", sa_relationship_kwargs={"cascade": "delete"})

class Course(SQLModel, table=True):

    id: int = Field(primary_key=True)
    name: str
    code: str
    description: str

    # Foreign Key & Many to one Relationship with Program
    program_id: int = Field(foreign_key="program.id")
    program: Program = Relationship(back_populates="courses")

    # TODO: Add relationship with quizzes, students, instructors, and maybe grades
