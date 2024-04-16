from fastapi import APIRouter, HTTPException, Query

from app.crud.user_crud import student_crud
from app.api.deps import AsyncSessionDep
from app.models.user_model import Student
from app.core.config import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.post("/student")
async def create_new_student(student: Student, session: AsyncSessionDep):
    logger.info("%s.create_a_student: %s", __name__, student)
    try:
        created_student = await student_crud.create_student(student=student, db=session)
        return created_student
    except (
        HTTPException
    ) as http_err:  # Catching the custom ValueError raised from CRUD operations
        logger.error(f"Error creating student: {http_err}")
        raise http_err
    except Exception as e:  # Catching any unexpected errors
        logger.error(f"Unexpected error creating student: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("", response_model=list[Student])
async def get_all_universities(
    db: AsyncSessionDep,
    offset: int = Query(default=0, le=10),
    limit: int = Query(default=10, le=100),
):
    """
    Get All Universities

    (Args):
        db: AsyncSession: Database session DI(Injected by FastAPI)
        offset: int: Offset for pagination
        limit: int: Limit for pagination

    (Returns):
        list[UniversityRead]: List of all Universities (Id and timestamps included)
    """
    try:
        all_students = await student_crud.get_all_students(
            db=db, offset=offset, limit=limit
        )
        return all_students
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/student/{student_id}")
async def delete_student_by_id(student_id: int, session: AsyncSessionDep):
    """
    Delete a student by ID.

    Args:
        student_id (int): The ID of the student to delete.
    """
    logger.info("%s.delete_topic_by_id: %s", __name__, student_id)
    try:
        return await student_crud.delete_student(id=student_id, db=session)
    except HTTPException as http_err:
        logger.error(f"Error deleting student: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error deleting student: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete student.")
