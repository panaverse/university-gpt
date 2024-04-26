from sqlmodel import SQLModel, Relationship
from typing import TYPE_CHECKING
from app.models.base import BaseIdModel

if TYPE_CHECKING:
    from app.models.program_models import Program

# Response Model examples
example_input_uni = {
    "name": "University of PIAIC",
    "description": "The University of PIAIC is a leading educational institution in Pakistan.",
}

example_output_uni = {
    "id": 1,
    "name": "University of PIAIC",
    "description": "The University of PIAIC is a leading educational institution in Pakistan.",
}


# Model for UniversityBase with common fields
class UniversityBase(SQLModel):
    name: str
    description: str | None = None


# Model for creating a University in the database
class University(BaseIdModel, UniversityBase, table=True):
    # 1. Relationship with Program
    programs: list["Program"] = Relationship(back_populates="university")


# Model for reading a University from the database this will be send as response back to the client
class UniversityRead(UniversityBase):
    id: int

    class ConfigDict:
        json_schema_extra = {"example": example_output_uni}


# Model for creating a University this will be to get data from the client
class UniversityCreate(UniversityBase):

    class ConfigDict:
        json_schema_extra = {"example": example_input_uni}


# Model for updating a University this will be to get data from the client
class UniversityUpdate(SQLModel):

    name: str | None = None
    description: str | None = None

    class ConfigDict:
        json_schema_extra = {"example": example_input_uni}