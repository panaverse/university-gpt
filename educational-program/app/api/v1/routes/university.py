from fastapi import APIRouter, Query, HTTPException

from app.models.university_models import UniversityRead, UniversityCreate, UniversityUpdate, PaginatedUniversityRead
from app.api.deps import DBSessionDep
from app.crud.university_crud import university_crud


# ------------------------------------------------
# University Endpoints
# ------------------------------------------------

router_uni = APIRouter()


@router_uni.post("", response_model=UniversityRead)
def create_new_university(
    university: UniversityCreate, db: DBSessionDep
) -> UniversityRead:
    """
    Create a new University in the database

    (Args):
        university: University: New University to create (from request body)

    (Returns):
        University: University that was created (with Id and timestamps included)
    """
    try:
        return university_crud.create_university_db(university=university, db=db)
    except HTTPException as http_e:
        # If the service layer raised an HTTPException, re-raise it
        raise http_e
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router_uni.get("", response_model=PaginatedUniversityRead)
def get_all_universities(
    db: DBSessionDep,
    page: int = Query(1, description="Page number", ge=1),
    per_page: int = Query(10, description="Items per page", ge=1, le=100)
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
        # Calculate the offset to skip the appropriate number of items
        offset = (page - 1) * per_page
        all_records = university_crud.get_all_universities_db(db=db, offset=offset, per_page=per_page)
        count_recs = university_crud.count_records(db=db)

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


@router_uni.get("/{university_id}", response_model=UniversityRead)
def get_university_by_id(
    university_id: int, db: DBSessionDep
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
        university = university_crud.get_university_by_id_db(
            university_id=university_id, db=db
        )
        return university
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_uni.patch("/{university_id}", response_model=UniversityRead)
def update_university_by_id(
    university_id: int, university: UniversityUpdate, db: DBSessionDep
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
    return university_crud.update_university_db(
        university_id=university_id, university=university, db=db
    )


@router_uni.delete("/{university_id}", response_model=dict)
def delete_university_by_id(university_id: int, db: DBSessionDep):
    """
    Delete a University by ID
    Args:
        university_id: int: ID of the University to delete
        db: AsyncSession: Database session
    Returns:
        University: University that was deleted
    """
    return university_crud.delete_university_db(
        university_id=university_id, db=db
    )


