from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.db import get_session
from services.quiz.university.crud import (
    create_university,create_program,create_course,
    read_universities,read_programs,read_courses,
    read_university,read_program,read_course,
    update_university,update_program,update_course,
    delete_university,delete_program,delete_course,
)
from services.quiz.university.models import (
    UniversityCreate, UniversityRead, UniversityUpdate,
    ProgramCreate, ProgramRead, ProgramUpdate,
    CourseCreate, CourseRead, CourseUpdate,
)

university_router = APIRouter()

@university_router.post("", response_model=UniversityRead)
async def create_a_university(university: UniversityCreate, db: AsyncSession = Depends(get_session)):
    return await create_university(university=university, db=db)


@university_router.get("", response_model=list[UniversityRead])
async def get_universities(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: AsyncSession = Depends(get_session),
):
    return await read_universities(offset=offset, limit=limit, db=db)


@university_router.get("/{university_id}", response_model=UniversityRead)
async def get_a_university(university_id: int, db: AsyncSession = Depends(get_session)):
    return await read_university(university_id=university_id, db=db)


@university_router.patch("/{university_id}", response_model=UniversityRead)
async def update_a_university(university_id: int, university: UniversityUpdate, db: AsyncSession = Depends(get_session)):
    return await update_university(university_id=university_id, university=university, db=db)


@university_router.delete("/{university_id}")
async def delete_a_university(university_id: int, db: AsyncSession = Depends(get_session)):
    return await delete_university(university_id=university_id, db=db)


program_router = APIRouter()

@program_router.post("", response_model=ProgramRead)
async def create_a_program(program: ProgramCreate, db: AsyncSession = Depends(get_session)):
    return await create_program(program=program, db=db)

@program_router.get("", response_model=list[ProgramRead])
async def get_programs(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: AsyncSession = Depends(get_session),
):
    return await read_programs(offset=offset, limit=limit, db=db)

@program_router.get("/{program_id}", response_model=ProgramRead)
async def get_a_program(program_id: int, db: AsyncSession = Depends(get_session)):
    return await read_program(program_id=program_id, db=db)

@program_router.patch("/{program_id}", response_model=ProgramRead)
async def update_a_program(program_id: int, program: ProgramUpdate, db: AsyncSession = Depends(get_session)):
    return await update_program(program_id=program_id, program=program, db=db)

@program_router.delete("/{program_id}")
async def delete_a_program(program_id: int, db: AsyncSession = Depends(get_session)):
    return await delete_program(program_id=program_id, db=db)


course_router = APIRouter()

@course_router.post("", response_model=CourseRead)
async def create_a_course(course: CourseCreate, db: AsyncSession = Depends(get_session)):
    return await create_course(course=course, db=db)

@course_router.get("", response_model=list[CourseRead])
async def get_courses(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: AsyncSession = Depends(get_session),
):
    return await read_courses(offset=offset, limit=limit, db=db)

@course_router.get("/{course_id}", response_model=CourseRead)
async def get_a_course(course_id: int, db: AsyncSession = Depends(get_session)):
    return await read_course(course_id=course_id, db=db)

@course_router.patch("/{course_id}", response_model=CourseRead)
async def update_a_course(course_id: int, course: CourseUpdate, db: AsyncSession = Depends(get_session)):
    return await update_course(course_id=course_id, course=course, db=db)

@course_router.delete("/{course_id}")
async def delete_a_course(course_id: int, db: AsyncSession = Depends(get_session)):
    return await delete_course(course_id=course_id, db=db)

router = APIRouter()
router.include_router(university_router, prefix="/university", tags=["University"])
router.include_router(program_router, prefix="/program", tags=["Program"])
router.include_router(course_router, prefix="/course", tags=["Course"])