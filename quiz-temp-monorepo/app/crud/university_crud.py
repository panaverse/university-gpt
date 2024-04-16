from fastapi import HTTPException
from sqlmodel import select
from app.core.db import AsyncSession

from app.models.university_model import (
    University,
    UniversityCreate,
    UniversityUpdate,
    Program,
    ProgramCreate,
    ProgramUpdate,
    Course,
    CourseCreate,
    CourseUpdate,
)


# ------------------------------------------------
# University CRUD
# ------------------------------------------------


class UniversityCRUD:
    async def create_university_db(
        self, *, university: UniversityCreate, db: AsyncSession
    ):
        """
        Create a new University in the database
        Args:
            university: UniversityCreate: New University to create (from request body)
            db: AsyncSession: Database session
        Returns:
            University: University that was created (with Id and timestamps included)
        """
        obj_in = University.model_validate(university)
        db.add(obj_in)
        await db.commit()
        await db.refresh(obj_in)
        return obj_in

    async def get_all_universities_db(
        self, *, db: AsyncSession, offset: int, limit: int
    ):
        """
        Get All Universities
        Args:
        db: AsyncSession: Database session
        Returns:
            University: List of all Universities (Id and timestamps included)
        """
        universities = await db.exec(select(University).offset(offset).limit(limit))
        print(universities)
        all_universities = universities.all()
        if all_universities is None:
            raise HTTPException(status_code=404, detail="Universities not found")
        return all_universities

    async def get_university_by_id_db(self, *, university_id: int, db: AsyncSession):
        """
        Get a University by ID
        Args:
            university_id: int: ID of the University to retrieve
            db: AsyncSession: Database session
        Returns:
            University: University that was retrieved
        """
        university = await db.get(University, university_id)
        if university is None:
            raise HTTPException(status_code=404, detail="University not found")
        return university

    async def update_university_db(
        self, *, university_id: int, university: UniversityUpdate, db: AsyncSession
    ):
        """
        Update a University by ID
        Args:
            university_id: int: ID of the University to update
            university: UniversityUpdate: New values for University
            db: AsyncSession: Database session
        Returns:
            University: University that was updated (with Id and timestamps included)
        """
        db_university = await db.get(University, university_id)
        if not db_university:
            raise HTTPException(status_code=404, detail="university not found")
        university_data = university.model_dump(exclude_unset=True)
        db_university.sqlmodel_update(university_data)
        print(university_data)
        db.add(db_university)

        await db.commit()
        await db.refresh(db_university)
        return db_university

    async def delete_university_db(self, *, university_id: int, db: AsyncSession):
        """
        Delete a University by ID
        Args:
            university_id: int: ID of the University to delete
            db: AsyncSession: Database session
        Returns:
            University: University that was deleted
        """
        university = await db.get(University, university_id)
        if university is None:
            raise HTTPException(status_code=404, detail="University not found")
        await db.delete(university)
        await db.commit()
        # return university
        return {"message": "University deleted"}


# ------------------------------------------------
# Program CRUD
# ------------------------------------------------


class ProgramCRUD:
    async def create_program_db(self, *, program: ProgramCreate, db: AsyncSession):
        """
        Create a new Program in the database
        Args:
            program: ProgramCreate: New Program to create (from request body)
            db: AsyncSession: Database session
        Returns:
            Program: Program that was created (with Id and timestamps included)
        """
        obj_in = Program.model_validate(program)
        db.add(obj_in)
        await db.commit()
        await db.refresh(obj_in)
        return obj_in

    # Get all Programs
    async def get_all_programs_db(self, *, db: AsyncSession, offset: int, limit: int):
        """
        Get All Programs
        Args:
        db: AsyncSession: Database session
        Returns:
        list[ProgramRead]: List of all Programs (Id and timestamps included)
        """
        stmt = select(Program).offset(offset).limit(limit)
        programs_req = await db.exec(stmt)
        programs = programs_req.all()
        return programs

    # Get Program by ID
    async def get_program_by_id_db(self, *, program_id: int, db: AsyncSession):
        """
        Get a Program by ID
        Args:
            program_id: int: ID of the Program to retrieve
            db: AsyncSession: Database session
        Returns:
            Program: Program that was retrieved
        """
        program = await db.get(Program, program_id)
        return program

    # Update Program by ID
    async def update_program_db(
        self, *, program_id: int, program: ProgramUpdate, db: AsyncSession
    ):
        """
        Update a Program by ID
        Args:
            program_id: int: ID of the Program to update
            program: ProgramUpdate: New values for Program
            db: AsyncSession: Database session
        Returns:
            Program: Program that was updated (with Id and timestamps included)
        """
        db_program = await db.get(Program, program_id)
        if not db_program:
            raise HTTPException(status_code=404, detail="Program not found")

        program_data = program.model_dump(exclude_unset=True)
        db_program.sqlmodel_update(program_data)
        db.add(db_program)

        await db.commit()
        await db.refresh(db_program)

        return db_program

    # Delete Program by ID
    async def delete_program_db(self, *, program_id: int, db: AsyncSession):
        """
        Delete a Program by ID
        Args:
            program_id: int: ID of the Program to delete
            db: AsyncSession: Database session
        Returns:
            Program: Program that was deleted
        """
        program = await db.get(Program, program_id)
        if program is None:
            raise HTTPException(status_code=404, detail="Program not found")
        await db.delete(program)
        await db.commit()
        # return program
        return {"message": "Program deleted"}


# ------------------------------------------------
# Course CRUD
# ------------------------------------------------


class CourseCRUD:
    async def create_course_db(self, *, course: CourseCreate, db: AsyncSession):
        """
        Create a new Course in the database
        Args:
            course: CourseCreate: New Course to create (from request body)
            db: AsyncSession: Database session
        Returns:
            Course: Course that was created (with Id and timestamps included)
        """
        obj_in = Course.model_validate(course)
        db.add(obj_in)
        await db.commit()
        await db.refresh(obj_in)
        return obj_in

    # Get all Courses
    async def get_all_courses_db(self, *, db: AsyncSession, offset: int, limit: int):
        """
        Get All Courses
        Args:
            db: AsyncSession: Database session
        Returns:
            list[CourseRead]: List of all Courses (Id and timestamps included)
        """
        courses_req = await db.exec(select(Course).offset(offset).limit(limit))
        courses = courses_req.all()
        if courses is None:
            raise HTTPException(status_code=404, detail="Courses not found")
        return courses

    # Get Course by ID
    async def get_course_by_id_db(self, *, course_id: int, db: AsyncSession):
        """
        Get a Course by ID
        Args:
            course_id: int: ID of the Course to retrieve
            db: AsyncSession: Database session
        Returns:
            Course: Course that was retrieved
        """
        course = await db.get(Course, course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return course

    # Update Course by ID
    async def update_course_db(
        self, *, course_id: int, course: CourseUpdate, db: AsyncSession
    ):
        """
        Update a Course by ID
        Args:
            course_id: int: ID of the Course to update
            course: CourseUpdate: New values for Course
            db: AsyncSession: Database session
        Returns:
            Course: Course that was updated (with Id and timestamps included)
        """
        db_course = await db.get(Course, course_id)
        if not db_course:
            raise HTTPException(status_code=404, detail="Course not found")
        course_data = course.model_dump(exclude_unset=True)
        db_course.sqlmodel_update(course_data)

        db.add(db_course)
        await db.commit()
        await db.refresh(db_course)

        return db_course

    # Delete Course by ID
    async def delete_course_db(self, *, course_id: int, db: AsyncSession):
        """
        Delete a Course by ID
        Args:
            course_id: int: ID of the Course to delete
            db: AsyncSession: Database session
        Returns:
            Course: Course that was deleted
        """
        course = await db.get(Course, course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        await db.delete(course)
        await db.commit()
        return {"message": "Course deleted"}


university_crud = UniversityCRUD()
program_crud = ProgramCRUD()
course_crud = CourseCRUD()
