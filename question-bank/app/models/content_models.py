from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import TYPE_CHECKING

from app.models.base import BaseIdModel

if TYPE_CHECKING:
    from app.models.topic_models import Topic
    

# Response Model examples
example_input_content = {"content_text": "Python programming language", "topic_id": 1}

example_output_content = {
    "id": 1,
    "content_desc": "Python programming language",
    "topic_id": 1,
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z",
}


class ContentBase(SQLModel):
    topic_id: int | None = Field(foreign_key="topic.id", default=None, index=True)
    content_text: str


class Content(BaseIdModel, ContentBase, table=True):
    # Topic Relationship
    topic: "Topic" = Relationship(
        back_populates="contents", sa_relationship_kwargs={"lazy": "joined"}
    )  


class ContentCreate(ContentBase):
    pass

    class Config:
        json_schema_extra = {"example": example_input_content}


class ContentResponse(ContentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {"example": example_output_content}


class ContentUpdate(SQLModel):
    topic_id: int | None = None
    content_text: str | None = None

    class Config:
        json_schema_extra = {"example": example_input_content}