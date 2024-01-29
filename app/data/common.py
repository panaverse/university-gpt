from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime
import enum

class TimestampMixin:
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserType(enum.Enum):
    ADMIN = "admin"
    MOD = "mod"
    STUDENT = "student"
    INSTRUCTOR = "instructor"    

class QuizStatusEnum(enum.Enum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED = "SUBMITTED"
    COMPLETED = "COMPLETED"


class QuestionDifficultyEnum(enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Base(DeclarativeBase, TimestampMixin):
    pass
