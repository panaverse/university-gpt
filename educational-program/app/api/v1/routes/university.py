from fastapi import APIRouter, Query, HTTPException

from app.models.university_models import UniversityRead, UniversityCreate, UniversityUpdate
from app.api.deps import DBSessionDep
from app.crud.university_crud import university_crud


# ------------------------------------------------
# University Endpoints
# ------------------------------------------------

router_uni = APIRouter()


@router_uni.post("", response_model=UniversityRead)
async def create_new_university(
    university: UniversityCreate, db: DBSessionDep
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
    db: DBSessionDep,
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
    return await university_crud.update_university_db(
        university_id=university_id, university=university, db=db
    )


@router_uni.delete("/{university_id}", response_model=dict)
async def delete_university_by_id(university_id: int, db: DBSessionDep):
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


