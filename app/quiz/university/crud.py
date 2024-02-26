from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.quiz.university.models import (
    University, UniversityCreate, UniversityRead, UniversityUpdate,
    Program, ProgramCreate, ProgramRead, ProgramUpdate,
    Course, CourseCreate, CourseRead, CourseUpdate
)


#------------------------------------------------
            #University CRUD
#------------------------------------------------

# Create a new University
async def create_university_db(university: UniversityCreate, db: AsyncSession) -> UniversityRead:
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

# Get all Universities
async def get_all_universities_db(db: AsyncSession, offset: int, limit: int) -> list[UniversityRead]:
    """
    Get All Universities
    Args:
    db: AsyncSession: Database session
    Returns:
    list[UniversityRead]: List of all Universities (Id and timestamps included)
    """
    stmt = select(University).offset(offset).limit(limit)
    universities = await db.execute(stmt)
    universities = universities.scalars().all()
    return universities

# Get University by ID
async def get_university_by_id_db(university_id: int, db: AsyncSession) -> UniversityRead:
    """
    Get a University by ID
    Args:
    university_id: int: ID of the University to retrieve
    db: AsyncSession: Database session
    Returns:
    University: University that was retrieved
    """
    stmt = select(University).where(University.id == university_id)
    university = await db.execute(stmt)
    university = university.scalar()
    return university

# Update University by ID
async def update_university_db(university_id: int, university: UniversityUpdate, db: AsyncSession) -> UniversityRead:
    """
    Update a University by ID
    Args:
    university_id: int: ID of the University to update
    university: UniversityUpdate: New values for University
    db: AsyncSession: Database session
    Returns:
    University: University that was updated (with Id and timestamps included)
    """
    db_university = db.get(University, university_id)
    if not db_university:
        raise HTTPException(status_code=404, detail="StudentGrade not found")
    university_data = university.model_dump(exclude_unset=True)
    for key, value in university_data.items():
        setattr(db_university, key, value)
    db.add(db_university)
    await db.commit()
    await db.refresh(db_university)
    return db_university

# Delete University by ID
async def delete_university_db(university_id: int, db: AsyncSession) -> UniversityRead:
    """
    Delete a University by ID
    Args:
    university_id: int: ID of the University to delete
    db: AsyncSession: Database session
    Returns:
    University: University that was deleted
    """
    stmt = select(University).where(University.id == university_id)
    university = await db.execute(stmt)
    university = university.scalar()
    if university is None:
        raise HTTPException(status_code=404, detail="University not found")
    db.delete(university)
    await db.commit()
    return university

#------------------------------------------------
            #Program CRUD
#------------------------------------------------

# Create a new Program
async def create_program_db(program: ProgramCreate, db: AsyncSession) -> ProgramRead:
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
async def get_all_programs_db(db: AsyncSession, offset: int, limit: int) -> list[ProgramRead]:
    """
    Get All Programs
    Args:
    db: AsyncSession: Database session
    Returns:
    list[ProgramRead]: List of all Programs (Id and timestamps included)
    """
    stmt = select(Program).offset(offset).limit(limit)
    programs = await db.execute(stmt)
    programs = programs.scalars().all()
    return programs

# Get Program by ID
async def get_program_by_id_db(program_id: int, db: AsyncSession) -> ProgramRead:
    """
    Get a Program by ID
    Args:
    program_id: int: ID of the Program to retrieve
    db: AsyncSession: Database session
    Returns:
    Program: Program that was retrieved
    """
    stmt = select(Program).where(Program.id == program_id)
    program = await db.execute(stmt)
    program = program.scalar()
    return program

# Update Program by ID
async def update_program_db(program_id: int, program: ProgramUpdate, db: AsyncSession) -> ProgramRead:
    """
    Update a Program by ID
    Args:
    program_id: int: ID of the Program to update
    program: ProgramUpdate: New values for Program
    db: AsyncSession: Database session
    Returns:
    Program: Program that was updated (with Id and timestamps included)
    """
    db_program = db.get(Program, program_id)
    if not db_program:
        raise HTTPException(status_code=404, detail="Program not found")
    program_data = program.model_dump(exclude_unset=True)
    for key, value in program_data.items():
        setattr(db_program, key, value)
    db.add(db_program)
    await db.commit()
    await db.refresh(db_program)
    return db_program

# Delete Program by ID
async def delete_program_db(program_id: int, db: AsyncSession) -> ProgramRead:
    """
    Delete a Program by ID
    Args:
    program_id: int: ID of the Program to delete
    db: AsyncSession: Database session
    Returns:
    Program: Program that was deleted
    """
    stmt = select(Program).where(Program.id == program_id)
    program = await db.execute(stmt)
    program = program.scalar()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    db.delete(program)
    await db.commit()
    return program

#------------------------------------------------
            #Course CRUD
#------------------------------------------------

# Create a new Course
async def create_course_db(course: CourseCreate, db: AsyncSession) -> CourseRead:
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
async def get_all_courses_db(db: AsyncSession, offset: int, limit: int) -> list[CourseRead]:
    """
    Get All Courses
    Args:
    db: AsyncSession: Database session
    Returns:
    list[CourseRead]: List of all Courses (Id and timestamps included)
    """
    stmt = select(Course).offset(offset).limit(limit)
    courses = await db.execute(stmt)
    courses = courses.scalars().all()
    return courses

# Get Course by ID
async def get_course_by_id_db(course_id: int, db: AsyncSession) -> CourseRead:
    """
    Get a Course by ID
    Args:
    course_id: int: ID of the Course to retrieve
    db: AsyncSession: Database session
    Returns:
    Course: Course that was retrieved
    """
    stmt = select(Course).where(Course.id == course_id)
    course = await db.execute(stmt)
    course = course.scalar()
    return course

# Update Course by ID
async def update_course_db(course_id: int, course: CourseUpdate, db: AsyncSession) -> CourseRead:
    """
    Update a Course by ID
    Args:
    course_id: int: ID of the Course to update
    course: CourseUpdate: New values for Course
    db: AsyncSession: Database session
    Returns:
    Course: Course that was updated (with Id and timestamps included)
    """
    db_course = db.get(Course, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    course_data = course.model_dump(exclude_unset=True)
    for key, value in course_data.items():
        setattr(db_course, key, value)
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

# Delete Course by ID
async def delete_course_db(course_id: int, db: AsyncSession) -> CourseRead:
    """
    Delete a Course by ID
    Args:
    course_id: int: ID of the Course to delete
    db: AsyncSession: Database session
    Returns:
    Course: Course that was deleted
    """
    stmt = select(Course).where(Course.id == course_id)
    course = await db.execute(stmt)
    course = course.scalar()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    await db.commit()
    return course

