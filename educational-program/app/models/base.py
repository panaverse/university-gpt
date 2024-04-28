from sqlmodel import SQLModel, Field
from datetime import datetime


class BaseIdModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True, index=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.now}
    )