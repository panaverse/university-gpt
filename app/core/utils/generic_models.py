import enum
from sqlmodel import SQLModel, Field
from datetime import datetime

class BaseIdModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True, index=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )

# Enum for QuestionDifficulty
class QuestionDifficultyEnum(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

# Enum for QuestionType
class QuestionTypeEnum(str, enum.Enum):
    # Single Select MCQ
    single_select_mcq = "single_select_mcq"
    # Multiple Select MCQ
    multiple_select_mcq = "multiple_select_mcq"