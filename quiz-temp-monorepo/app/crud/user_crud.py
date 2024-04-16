from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel import select

from app.core.db import AsyncSession
from app.models.user_model import Student
from app.core.config import logger_config

logger = logger_config(__name__)


class StudentCRUD:
    async def create_student(self, *, student: Student, db: AsyncSession):
        try:
            student_in_db = Student.model_validate(student)

            db.add(student_in_db)
            await db.commit()
            await db.refresh(student_in_db)

            return student_in_db

        except IntegrityError as e:
            await db.rollback()  # Ensure rollback is awaited
            logger.error(
                f"CREATE_STUDENT: An integrity error occurred while creating the student: {e}"
            )
            raise HTTPException(status_code=500, detail="Data integrity issue.") from e

        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(
                f"CREATE_STUDENT: A database error occurred while creating the student: {e}"
            )
            raise HTTPException(
                status_code=500, detail="Database operation failed."
            ) from e

        except Exception as e:
            await db.rollback()
            logger.error(f"CREATE_STUDENT: An unexpected error occurred: {e}")
            raise HTTPException(
                status_code=500, detail="An unexpected error occurred."
            ) from e

    async def get_all_students(self, *, db: AsyncSession, offset: int, limit: int):
        try:
            students = await db.exec(select(Student).offset(offset).limit(limit))
            return students.all()
        except Exception as e:
            logger.error(f"GET_ALL_STUDENTS: An unexpected error occurred: {e}")
            raise HTTPException(
                status_code=500, detail="An unexpected error occurred."
            ) from e

    async def delete_student(self, *, id: int, db: AsyncSession):
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
                    status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
                )
            await db.delete(student)
            await db.commit()
            return {"message": "Student deleted successfully"}
        except HTTPException:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
            )
        except Exception as e:
            await db.rollback()
            print(f"Error deleting student: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting student",
            )


student_crud = StudentCRUD()
