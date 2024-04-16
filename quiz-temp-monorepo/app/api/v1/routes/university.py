from fastapi import APIRouter, Query, HTTPException

from app.api.deps import AsyncSessionDep
from app.crud.university_crud import university_crud, course_crud, program_crud
from app.models.university_model import (
    UniversityRead,
    UniversityCreate,
    UniversityUpdate,
    ProgramRead,
    ProgramCreate,
    ProgramUpdate,
    CourseRead,
    CourseCreate,
    CourseUpdate,
)


# ------------------------------------------------
# University Endpoints
# ------------------------------------------------

router_uni = APIRouter()


@router_uni.post("", response_model=UniversityRead)
async def create_new_university(
    university: UniversityCreate, db: AsyncSessionDep
) -> UniversityRead:
    """
    Create a new University in the database

    (Args):
        university: University: New University to create (from request body)

    (Returns):
        University: University that was created (with Id and timestamps included)
    """
    return await university_crud.create_university_db(university=university, db=db)


@router_uni.get("", response_model=list[UniversityRead])
async def get_all_universities(
    db: AsyncSessionDep,
    offset: int = Query(default=0, le=10),
    limit: int = Query(default=10, le=100),
) -> list[UniversityRead]:
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
        all_universities = await university_crud.get_all_universities_db(
            db=db, offset=offset, limit=limit
        )
        return all_universities
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_uni.get("/{university_id}", response_model=UniversityRead)
async def get_university_by_id(
    university_id: int, db: AsyncSessionDep
) -> UniversityRead:
    """
    Get a University by ID
    Args:
    university_id: int: ID of the University to retrieve
    db: AsyncSession: Database session DI(Injected by FastAPI)
    Returns:
    University: University that was retrieved
    """
    try:
        university = await university_crud.get_university_by_id_db(
            university_id=university_id, db=db
        )
        return university
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_uni.patch("/{university_id}", response_model=UniversityRead)
async def update_university_by_id(
    university_id: int, university: UniversityUpdate, db: AsyncSessionDep
) -> UniversityRead:
    """
    Update a University by ID
    Args:
        university_id: int: ID of the University to update
        university: UniversityUpdate: New values for University
        db: AsyncSession: Database session
    Returns:
        University: University that was updated (with Id and timestamps included)
    """
    return await university_crud.update_university_db(
        university_id=university_id, university=university, db=db
    )


@router_uni.delete("/{university_id}", response_model=dict)
async def delete_university_by_id(university_id: int, db: AsyncSessionDep):
    """
    Delete a University by ID
    Args:
        university_id: int: ID of the University to delete
        db: AsyncSession: Database session
    Returns:
        University: University that was deleted
    """
    return await university_crud.delete_university_db(
        university_id=university_id, db=db
    )


# ------------------------------------------------
# Program Endpoints
# ------------------------------------------------

router_prog = APIRouter()


# Endpoints for creating a new Program
@router_prog.post("", response_model=ProgramRead)
async def create_new_program(
    program: ProgramCreate, db: AsyncSessionDep
) -> ProgramRead:
    """
    Create a new Program in the database

    (Args):
        program: Program: New Program to create (from request body)

    (Returns):
        Program: Program that was created (with Id and timestamps included)
    """
    try:
        return await program_crud.create_program_db(program=program, db=db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for getting all Programs
@router_prog.get("", response_model=list[ProgramRead])
async def get_all_programs(
    db: AsyncSessionDep,
    offset: int = Query(default=0, le=10),
    limit: int = Query(default=10, le=100),
) -> list[ProgramRead]:
    """
    Get All Programs

    (Args):
        db: AsyncSession: Database session DI(Injected by FastAPI)
        offset: int: Offset for pagination
        limit: int: Limit for pagination

    (Returns):
        list[ProgramRead]: List of all Programs (Id and timestamps included)
    """
    try:
        all_programs = await program_crud.get_all_programs_db(
            db=db, offset=offset, limit=limit
        )
        return all_programs
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for getting a Program by ID
@router_prog.get("/{program_id}", response_model=ProgramRead)
async def get_program_by_id(program_id: int, db: AsyncSessionDep) -> ProgramRead:
    """
    Get a Program by ID
    Args:
    program_id: int: ID of the Program to retrieve
    db: AsyncSession: Database session DI(Injected by FastAPI)
    Returns:
    Program: Program that was retrieved
    """
    try:
        program = await program_crud.get_program_by_id_db(program_id=program_id, db=db)
        if program is None:
            raise HTTPException(status_code=404, detail="Program not found")
        return program
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for updating a Program by ID
@router_prog.patch("/{program_id}", response_model=ProgramRead)
async def update_program_by_id(
    program_id: int, program: ProgramUpdate, db: AsyncSessionDep
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
    try:
        return await program_crud.update_program_db(
            program_id=program_id, program=program, db=db
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_prog.delete("/{program_id}")
async def delete_program_by_id(program_id: int, db: AsyncSessionDep):
    """
    Delete a Program by ID
    Args:
        program_id: int: ID of the Program to delete
        db: AsyncSession: Database session
    Returns:
        Program: Program that was deleted
    """
    return await program_crud.delete_program_db(program_id=program_id, db=db)


# ------------------------------------------------
# Course Endpoints
# ------------------------------------------------

router_course = APIRouter()


# Endpoints for creating a new Course
@router_course.post("", response_model=CourseRead)
async def create_new_course(course: CourseCreate, db: AsyncSessionDep) -> CourseRead:
    """
    Create a new Course in the database

    (Args):
        course: Course: New Course to create (from request body)

    (Returns):
        Course: Course that was created (with Id and timestamps included)
    """
    return await course_crud.create_course_db(course=course, db=db)


# Endpoints for getting all Courses
@router_course.get("", response_model=list[CourseRead])
async def get_all_courses(
    db: AsyncSessionDep,
    offset: int = Query(default=0, le=10),
    limit: int = Query(default=10, le=100),
) -> list[CourseRead]:
    """
    Get All Courses

    (Args):
        db: AsyncSession: Database session DI(Injected by FastAPI)
        offset: int: Offset for pagination
        limit: int: Limit for pagination

    (Returns):
        list[CourseRead]: List of all Courses (Id and timestamps included)
    """
    try:
        all_courses = await course_crud.get_all_courses_db(
            db=db, offset=offset, limit=limit
        )
        return all_courses
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for getting a Course by ID
@router_course.get("/{course_id}", response_model=CourseRead)
async def get_course_by_id(course_id: int, db: AsyncSessionDep) -> CourseRead:
    """
    Get a Course by ID
    Args:
    course_id: int: ID of the Course to retrieve
    db: AsyncSession: Database session DI(Injected by FastAPI)
    Returns:
    Course: Course that was retrieved
    """
    try:
        course = await course_crud.get_course_by_id_db(course_id=course_id, db=db)
        return course
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for updating a Course by ID
@router_course.patch("/{course_id}", response_model=CourseRead)
async def update_course_by_id(
    course_id: int, course: CourseUpdate, db: AsyncSessionDep
) -> CourseRead:
    """
    Update a Course by ID
    Args:
        course_id: int: ID of the Course to update
        course: CourseUpdate: New values for Course
        db: AsyncSession: Database session
    Returns:
        Course: Course that was updated (with Id and timestamps included)
    """
    return await course_crud.update_course_db(course_id=course_id, course=course, db=db)


@router_course.delete("/{course_id}")
async def delete_course_by_id(course_id: int, db: AsyncSessionDep):
    """
    Delete a Course by ID
    Args:
        course_id: int: ID of the Course to delete
        db: AsyncSession: Database session
    Returns:
        Course: Course that was deleted
    """
    return await course_crud.delete_course_db(course_id=course_id, db=db)


router = APIRouter()

router.include_router(router_uni, prefix="/university", tags=["University"])
router.include_router(router_prog, prefix="/program", tags=["Program"])
router.include_router(router_course, prefix="/course", tags=["Course"])
