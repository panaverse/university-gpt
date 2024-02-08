from sqlmodel import Field, SQLModel, Relationship  
from api.quiz.answersheet.models import AnswerSheet

class Student(SQLModel, table=True):
    student_id: int = Field(primary_key=True)

    answersheets: list['AnswerSheet'] = Relationship(back_populates="student")