from sqlmodel import Field, SQLModel

class QuizTopic(SQLModel, table=True):
    quiz_id: int | None = Field(
        foreign_key="quiz.id", default=None, index=True, primary_key=True
    )
    topic_id: int | None = Field(
        foreign_key="topic.id", default=None, index=True, primary_key=True
    )

    class Config:
        json_schema_extra = {"example": {"quiz_id": "1", "topic_id": "1"}}
