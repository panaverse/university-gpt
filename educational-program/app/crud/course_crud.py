from fastapi import HTTPException
from sqlmodel import select, Session
from app.models.course_models import Course, CourseCreate, CourseUpdate
from app.models.program_models import Program

class CourseCRUD:
    def create_course_db(self, *, course: CourseCreate, db: Session):
        """
        Create a new Course in the database
        Args:
            course: CourseCreate: New Course to create (from request body)
            db: Session: Database session
        Returns:
            Course: Course that was created (with Id and timestamps included)
        """
        # Verify if Program ID is present and valid
        if course.program_id:
            program = db.get(Program, course.program_id)
            if not program:
                raise HTTPException(status_code=404, detail="Invalid program ID")
        # Check if Course with Same name already exists
        course_exists = db.exec(select(Course).where(Course.name == course.name)).first()
        if course_exists:
            raise HTTPException(status_code=400, detail="Course with same name already exists")
        obj_in = Course.model_validate(course)
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    # Get all Courses
    def get_all_courses_db(self, *, db: Session, offset: int, per_page: int):
        """
        Get All Courses
        Args:
            db: Session: Database session
        Returns:
            list[CourseRead]: List of all Courses (Id and timestamps included)
        """
        if offset < 0:
            raise HTTPException(status_code=400, detail="Offset cannot be negative")
        if per_page < 1:
            raise HTTPException(status_code=400, detail="Per page items cannot be less than 1")
        
        courses = db.exec(select(Course).offset(offset).limit(per_page)).all()
        if courses is None:
            raise HTTPException(status_code=404, detail="Courses not found")
        return courses

    # Get Course by ID
    def get_course_by_id_db(self, *, course_id: int, db: Session):
        """
        Get a Course by ID
        Args:
            course_id: int: ID of the Course to retrieve
            db: Session: Database session
        Returns:
            Course: Course that was retrieved
        """
        course = db.get(Course, course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return course

    # Update Course by ID
    def update_course_db(
        self, *, course_id: int, course: CourseUpdate, db: Session
    ):
        """
        Update a Course by ID
        Args:
            course_id: int: ID of the Course to update
            course: CourseUpdate: New values for Course
            db: Session: Database session
        Returns:
            Course: Course that was updated (with Id and timestamps included)
        """
        db_course = db.get(Course, course_id)
        if not db_course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # If Program ID is present verify if it's valid and exists
        if course.program_id:
            program = db.get(Program, course.program_id)
            if not program:
                raise HTTPException(status_code=404, detail="Program not found")
        course_data = course.model_dump(exclude_unset=True)
        db_course.sqlmodel_update(course_data)

        db.add(db_course)
        db.commit()
        db.refresh(db_course)

        return db_course

    # Delete Course by ID
    def delete_course_db(self, *, course_id: int, db: Session):
        """
        Delete a Course by ID
        Args:
            course_id: int: ID of the Course to delete
            db: Session: Database session
        Returns:
            Course: Course that was deleted
        """
        course = db.get(Course, course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        db.delete(course)
        db.commit()
        return {"message": "Course deleted"}
    

    def count_records(self, *, db: Session) -> int:
        try:
            query = select(Course.name)
            items = db.exec(query).all()
            count = len(items)
            return count
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error counting SearchToolRecord items: {e}")
            # Re-raise the exception to be handled at the endpoint level
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


course_crud = CourseCRUD()