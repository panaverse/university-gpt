from fastapi import APIRouter, Query, HTTPException

from app.models.course_models import CourseCreate, CourseRead, CourseUpdate
from app.api.deps import DBSessionDep
from app.crud.course_crud import course_crud

router_course = APIRouter()


# Endpoints for creating a new Course
@router_course.post("", response_model=CourseRead)
async def create_new_course(course: CourseCreate, db: DBSessionDep) -> CourseRead:
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
    db: DBSessionDep,
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
async def get_course_by_id(course_id: int, db: DBSessionDep) -> CourseRead:
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
    course_id: int, course: CourseUpdate, db: DBSessionDep
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
async def delete_course_by_id(course_id: int, db: DBSessionDep):
    """
    Delete a Course by ID
    Args:
        course_id: int: ID of the Course to delete
        db: AsyncSession: Database session
    Returns:
        Course: Course that was deleted
    """
    return await course_crud.delete_course_db(course_id=course_id, db=db)