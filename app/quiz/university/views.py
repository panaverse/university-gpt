from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.quiz.university.models import (UniversityRead, UniversityCreate, UniversityUpdate,
                                        ProgramRead, ProgramCreate, ProgramUpdate,
                                        CourseRead, CourseCreate, CourseUpdate)
from app.quiz.university.crud import (create_university_db, get_all_universities_db,
                                      get_university_by_id_db, update_university_db,
                                      create_program_db, get_all_programs_db,
                                      get_program_by_id_db, update_program_db,
                                      create_course_db, get_all_courses_db,
                                      get_course_by_id_db, update_course_db)


#------------------------------------------------
            #University Endpoints
#------------------------------------------------

router_uni = APIRouter()

# Endpoints for creating a new University
@router_uni.post("", response_model=UniversityRead)
async def create_new_university(university: UniversityCreate, db: AsyncSession = Depends(get_session) )-> UniversityRead:
    """
    Create a new University in the database

    (Args):
        university: University: New University to create (from request body)
        
    (Returns):
        University: University that was created (with Id and timestamps included)
    """
    return await create_university_db(university, db=db)

# Endpoints for getting all Universities
@router_uni.get("", response_model=list[UniversityRead])
async def get_all_universities(db: AsyncSession = Depends(get_session), offset: int = Query(default=0, le=10), limit: int = Query(default=10, le=100)) -> list[UniversityRead]:
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
        all_universities = await get_all_universities_db(db, offset, limit)
        return all_universities
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoints for getting a University by ID
@router_uni.get("/{university_id}", response_model=UniversityRead)
async def get_university_by_id(university_id: int, db: AsyncSession = Depends(get_session)) -> UniversityRead:
    """
    Get a University by ID
    Args:
    university_id: int: ID of the University to retrieve
    db: AsyncSession: Database session DI(Injected by FastAPI)
    Returns:
    University: University that was retrieved
    """
    try:
        university = await get_university_by_id_db(university_id, db)
        if university is None:
            raise HTTPException(status_code=404, detail="University not found")
        return university
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints for updating a University by ID
@router_uni.put("/{university_id}", response_model=UniversityRead)
async def update_university_by_id(university_id: int, university: UniversityUpdate, db: AsyncSession = Depends(get_session))-> UniversityRead:
    """
    Update a University by ID
    Args:
    university_id: int: ID of the University to update
    university: UniversityUpdate: New values for University
    db: AsyncSession: Database session
    Returns:
    University: University that was updated (with Id and timestamps included)
    """
    return await update_university_db(university_id=university_id, university=university, db=db)

#------------------------------------------------
            #Program Endpoints
#------------------------------------------------

router_prog = APIRouter()

# Endpoints for creating a new Program
@router_prog.post("", response_model=ProgramRead)
async def create_new_program(program: ProgramCreate,  db: AsyncSession = Depends(get_session))-> ProgramRead:
    """
    Create a new Program in the database

    (Args):
        program: Program: New Program to create (from request body)
        
    (Returns):
        Program: Program that was created (with Id and timestamps included)
    """
    return await create_program_db(program, db=db)

# Endpoints for getting all Programs
@router_prog.get("", response_model=list[ProgramRead])
async def get_all_programs(db: AsyncSession = Depends(get_session), offset: int = Query(default=0, le=10), limit: int = Query(default=10, le=100)) -> list[ProgramRead]:
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
        all_programs = await get_all_programs_db(db, offset, limit)
        return all_programs
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoints for getting a Program by ID
@router_prog.get("/{program_id}", response_model=ProgramRead)
async def get_program_by_id(program_id: int, db: AsyncSession = Depends(get_session)) -> ProgramRead:
    """
    Get a Program by ID
    Args:
    program_id: int: ID of the Program to retrieve
    db: AsyncSession: Database session DI(Injected by FastAPI)
    Returns:
    Program: Program that was retrieved
    """
    try:
        program = await get_program_by_id_db(program_id, db)
        if program is None:
            raise HTTPException(status_code=404, detail="Program not found")
        return program
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints for updating a Program by ID
@router_prog.put("/{program_id}", response_model=ProgramRead)
async def update_program_by_id(program_id: int, program: ProgramUpdate,db:AsyncSession = Depends(get_session))-> ProgramRead:
    """
    Update a Program by ID
    Args:
    program_id: int: ID of the Program to update
    program: ProgramUpdate: New values for Program
    db: AsyncSession: Database session
    Returns:
    Program: Program that was updated (with Id and timestamps included)
    """
    return await update_program_db(program_id=program_id, program=program, db=db)

#------------------------------------------------
            #Course Endpoints
#------------------------------------------------

router_course = APIRouter()

# Endpoints for creating a new Course
@router_course.post("", response_model=CourseRead)
async def create_new_course(course: CourseCreate, db: AsyncSession = Depends(get_session))-> CourseRead:
    """
    Create a new Course in the database

    (Args):
        course: Course: New Course to create (from request body)
        
    (Returns):
        Course: Course that was created (with Id and timestamps included)
    """
    return await create_course_db(course, db=db)

# Endpoints for getting all Courses
@router_course.get("", response_model=list[CourseRead])
async def get_all_courses(db: AsyncSession = Depends(get_session), offset: int = Query(default=0, le=10), limit: int = Query(default=10, le=100)) -> list[CourseRead]:
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
        all_courses = await get_all_courses_db(db, offset, limit)
        return all_courses
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoints for getting a Course by ID
@router_course.get("/{course_id}", response_model=CourseRead)
async def get_course_by_id(course_id: int, db: AsyncSession = Depends(get_session)) -> CourseRead:
    """
    Get a Course by ID
    Args:
    course_id: int: ID of the Course to retrieve
    db: AsyncSession: Database session DI(Injected by FastAPI)
    Returns:
    Course: Course that was retrieved
    """
    try:
        course = await get_course_by_id_db(course_id, db)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return course
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoints for updating a Course by ID
@router_course.put("/{course_id}", response_model=CourseRead)
async def update_course_by_id(course_id: int, course: CourseUpdate,db:AsyncSession = Depends(get_session))-> CourseRead:
    """
    Update a Course by ID
    Args:
    course_id: int: ID of the Course to update
    course: CourseUpdate: New values for Course
    db: AsyncSession: Database session
    Returns:
    Course: Course that was updated (with Id and timestamps included)
    """
    return await update_course_db(course_id=course_id, course=course, db=db)


router = APIRouter()

router.include_router(router_uni, prefix="/university")
router.include_router(router_prog, prefix="/program")
router.include_router(router_course, prefix="/course")
