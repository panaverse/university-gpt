from sqlmodel import Field, SQLModel


class Student(SQLModel, table=True):
    student_id: int = Field(primary_key=True)
