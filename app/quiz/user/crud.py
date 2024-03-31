from fastapi import HTTPException, status
from sqlmodel import select, and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.database import AsyncSession
from app.quiz.user.models import Student
from app.core.utils.logger import logger_config

logger = logger_config(__name__)

# Create Student


async def create_student(student: Student, db: AsyncSession):
    try:
        student_in_db = Student.model_validate(student)

        db.add(student_in_db)
        await db.commit()
        db.refresh(student_in_db)

        return student_in_db

    except IntegrityError as e:
        await db.rollback()  # Ensure rollback is awaited
        logger.error(
            f"CREATE_STUDENT: An integrity error occurred while creating the student: {e}")
        raise HTTPException(
            status_code=500, detail="Data integrity issue.") from e

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(
            f"CREATE_STUDENT: A database error occurred while creating the student: {e}")
        raise HTTPException(
            status_code=500, detail="Database operation failed.") from e

    except Exception as e:
        await db.rollback()
        logger.error(f"CREATE_STUDENT: An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred.") from e

# Delete Student


async def delete_student(id: int, db: AsyncSession):
    """
    Deletes a student from the database based on the provided ID.

    Args:
        id (int): The ID of the student to be deleted.

    Raises:
        HTTPException: If the student with the provided ID is not found.

    Returns:
        dict: A dictionary with a message indicating the successful deletion of the student.
    """
    try:
        student = await db.get(Student, id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        await db.delete(student)
        await db.commit()
        return {"message": "Student deleted successfully"}
    except HTTPException:
        await db.rollback()
        raise e
    except Exception as e:
        await db.rollback()
        print(f"Error deleting student: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting student")
