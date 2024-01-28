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

class QuestionType(enum.Enum):
    SINGLE_SLETECT = "single_select"
    MULTIPE_SELECT = "multiple_select"
    FREE_TEXT = "free_text"
    CODING = "coding"  

class Base(DeclarativeBase, TimestampMixin):
    pass
