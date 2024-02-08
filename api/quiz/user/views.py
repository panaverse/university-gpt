from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from api.core.database import get_session, AsyncSession
from api.quiz.user.crud import create_student, delete_student
from api.quiz.user.models import Student
from api.core.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)

@router.post("/student")
async def create_new_student(student: Student, db: Annotated[AsyncSession, Depends(get_session)]):
    logger.info("%s.create_a_student: %s", __name__, student)
    try:
        created_student = await create_student(student=student, db=db)
        return created_student
    except HTTPException as http_err:  # Catching the custom ValueError raised from CRUD operations
        logger.error(f"Error creating student: {e}")
        raise http_err
    except Exception as e:  # Catching any unexpected errors
        logger.error(f"Unexpected error creating student: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@router.delete("/student/{student_id}")
async def delete_student_by_id(student_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """
    Delete a student by ID.

    Args:
        student_id (int): The ID of the student to delete.
    """
    logger.info("%s.delete_topic_by_id: %s", __name__, student_id)
    try:
        return await delete_student(id=student_id, db=db)
    except HTTPException as http_err:
        logger.error(f"Error deleting student: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error deleting student: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete student.")

