from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import Optional, Union

from app.models.base import BaseIdModel
from app.models.content_models import Content, ContentCreate, ContentResponse
from app.models.question_models import QuestionBank, QuestionBankRead

# Response Model examples
example_topic_input = {
    "parent_id": None,  # "None" for root topic
    "title": "Python",
    "course_id": 1,
    "description": "Python programming language",
}

example_topic_input_with_content = {
    "title": "OOP Paradigm",
    "description": "Learn OOPS in Python12",
    "course_id": 1,
    "parent_id": 1,  # This is Optional for Subtopics
    "contents": [
        {
            "content_text": "OOP is a programming paradigm based on classes and objects rather."
        },
        {
            "content_text": "OOP Pillars: Encapsulation, Inheritance and Polymorphism, and Abstraction."
        },
    ],
}


class TopicBase(SQLModel):
    title: str = Field(max_length=160, index=True)
    description: str
    parent_id: int | None = Field(
        foreign_key="topic.id",  # notice the lowercase "t" to refer to the database table name
        default=None,
    )
    # Relationship with Course
    course_id: int = Field( default=None) # In Single DB this will be foreign key

    class Config:
        json_schema_extra = example_topic_input


# It will include Topics, Subtopics, CaseStudies Given for Assessments


class Topic(BaseIdModel, TopicBase, table=True):
    children_topics: list["Topic"] = Relationship(back_populates="parent_topic")
    parent_topic: Optional["Topic"] = Relationship(
        back_populates="children_topics",
        sa_relationship_kwargs=dict(
            remote_side="Topic.id"  # notice the uppercase "T" to refer to this table class
        ),
    )

    # Content Table relationship to store the content of the topic
    contents: list["Content"] = Relationship(
        back_populates="topic",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"},
    )

    # QuestionBank Relationship
    questions: list["QuestionBank"] = Relationship(
        back_populates="topic", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class TopicCreate(TopicBase):
    contents: list["ContentCreate"] = []

    class Config:
        json_schema_extra = {"example": example_topic_input_with_content}


class TopicResponse(TopicBase):
    id: int
    parent_id: int | None = None
    course_id: int
    created_at: datetime
    updated_at: datetime


class TopicUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    parent_id: int | None = None
    course_id: int 

    class Config:
        json_schema_extra = {
            "example": {
                "title": "OOP Paradigm",
                "description": "Learn OOPS in Typescript 5.0+",
                "parent_id": 1,  # This is Optional for Subtopics
                "course_id": 1,
            }
        }


class TopicResponseWithContent(TopicResponse):
    contents: list["ContentResponse"] = []


class TopicResponseWithQuestions(TopicResponse):
    questions: list[QuestionBankRead] = []


class PaginatedTopicRead(SQLModel):
    """
    Represents a paginated list of SearchToolRecord items.
    """
    count: int
    next:  Union[str, None] = None
    previous:  Union[str, None] = None
    results: list[TopicResponse]