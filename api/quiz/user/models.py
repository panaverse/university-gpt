from sqlmodel import Field, SQLModel, Relationship  

class Student(SQLModel, table=True):
    student_id: int = Field(primary_key=True)