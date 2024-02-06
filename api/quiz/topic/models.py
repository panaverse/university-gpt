from sqlmodel import Field, Relationship, SQLModel, Column, DateTime
from datetime import datetime

from api.quiz.question.models import QuestionBank

from typing import Optional

class TopicBase(SQLModel):
    title: str = Field(max_length=160, index=True)
    description: str
    parent_id: int | None = Field(
        foreign_key='topic.id',  # notice the lowercase "t" to refer to the database table name
        default=None    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "OOPs in Typescript",
                "description": "Learn OOPS in Typescript 5.0+",
                "parent_id": 1 # This is Optional for Subtopics
            }
        }

# It will include Topics, Subtopics, CaseStudies Given for Assessments
class Topic(TopicBase, table=True):

    id: int | None = Field(default=None, primary_key=True, index=True)

    children_topic: list['Topic'] = Relationship(back_populates='parent_topic')
    parent_topic: Optional['Topic'] = Relationship(
        back_populates='children_topic',
        sa_relationship_kwargs=dict(
            remote_side='Topic.id'  # notice the uppercase "T" to refer to this table class
        )
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
            DateTime(timezone=True),
            onupdate=datetime.utcnow,
            nullable=False,
        ))

    # QuestionBank Relationship
    questions: list['QuestionBank'] = Relationship(
        back_populates='topic', sa_relationship_kwargs={"cascade": "delete"})
    # Relationship to the TempQuestions
    # temp_questions: list['TempQuestionBank'] = Relationship(
    #     back_populates='topic', sa_relationship_kwargs={"cascade": "delete"})

    # TODO: Add a Content Table & add relationship to store the content of the topic


class TopicCreate(TopicBase):
    pass


class TopicResponse(TopicBase):
    id: int
    parent_id: int | None = None
    created_at: datetime
    updated_at: datetime


class TopicUpdate(TopicBase):
    title: str | None = None
    description: str | None = None
    parent_id: int | None = None
