from enum import Enum
from typing import Literal

from pydantic import BaseModel


class Status(str, Enum):
    OK = "OK"
    NOT_OK = "NOT_OK"


class Health(BaseModel):
    app_status: Status | None
    db_status: Status | None
    environment: Literal["development", "staging", "production"] | str | None


class Stats(BaseModel):
    university: int | None
    program: int | None
    course: int | None
    topics: int | None
    questions: int | None
    quizzes: int | None
    quiz_settings: int | None
