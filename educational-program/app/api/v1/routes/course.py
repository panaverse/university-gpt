from fastapi import APIRouter, Query, HTTPException

from app.models.course_models import CourseCreate, CourseRead, CourseUpdate, PaginatedCourseRead
from app.api.deps import DBSessionDep
from app.crud.course_crud import course_crud

router_course = APIRouter()


# Endpoints for creating a new Course
@router_course.post("", response_model=CourseRead)
def create_new_course(course: CourseCreate, db: DBSessionDep) -> CourseRead:
    """
    Create a new Course in the database

    (Args):
        course: Course: New Course to create (from request body)

    (Returns):
        Course: Course that was created (with Id and timestamps included)
    """
    try:
        return course_crud.create_course_db(course=course, db=db)
    except HTTPException as http_e:
        # If the service layer raised an HTTPException, re-raise it
        raise http_e
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Endpoints for getting all Courses
@router_course.get("", response_model=PaginatedCourseRead)
def get_all_courses(
    db: DBSessionDep,
    page: int = Query(1, description="Page number", ge=1),
    per_page: int = Query(10, description="Items per page", ge=1, le=100)
) -> PaginatedCourseRead:
    """
    Get All Courses

    (Args):
        db: AsyncSession: Database session DI(Injected by FastAPI)
        offset: int: Offset for pagination
        limit: int: Limit for pagination

    (Returns):
        PaginatedCourseRead: List of all Courses (Id and timestamps included)
    """
    try:

        offset = (page - 1) * per_page
        all_records = course_crud.get_all_courses_db(db=db, offset=offset, per_page=per_page)
        count_recs = course_crud.count_records(db=db)

        # Calculate next and previous page URLs
        next_page = f"?page={page + 1}&per_page={per_page}" if len(all_records) == per_page else None
        previous_page = f"?page={page - 1}&per_page={per_page}" if page > 1 else None

        # Return data in paginated format
        paginated_data = {"count": count_recs, "next": next_page, "previous": previous_page, "all_records": all_records}
        return paginated_data
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for getting a Course by ID
@router_course.get("/{course_id}", response_model=CourseRead)
def get_course_by_id(course_id: int, db: DBSessionDep) -> CourseRead:
    """
    Get a Course by ID
    Args:
    course_id: int: ID of the Course to retrieve
    db: AsyncSession: Database session DI(Injected by FastAPI)
    Returns:
    Course: Course that was retrieved
    """
    try:
        course = course_crud.get_course_by_id_db(course_id=course_id, db=db)
        return course
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for updating a Course by ID
@router_course.patch("/{course_id}", response_model=CourseRead)
def update_course_by_id(
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
    return course_crud.update_course_db(course_id=course_id, course=course, db=db)


@router_course.delete("/{course_id}")
def delete_course_by_id(course_id: int, db: DBSessionDep):
    """
    Delete a Course by ID
    Args:
        course_id: int: ID of the Course to delete
        db: AsyncSession: Database session
    Returns:
        Course: Course that was deleted
    """
    return course_crud.delete_course_db(course_id=course_id, db=db)