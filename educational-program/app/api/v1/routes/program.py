from fastapi import APIRouter, Query, HTTPException

from app.models.program_models import ProgramCreate, ProgramRead, ProgramUpdate, PaginatedProgramRead
from app.api.deps import DBSessionDep
from app.crud.program_crud import program_crud

router_prog = APIRouter()


# Endpoints for creating a new Program
@router_prog.post("", response_model=ProgramRead)
def create_new_program(
    program: ProgramCreate, db: DBSessionDep
) -> ProgramRead:
    """
    Create a new Program in the database

    (Args):
        program: Program: New Program to create (from request body)

    (Returns):
        Program: Program that was created (with Id and timestamps included)
    """
    try:
        return program_crud.create_program_db(program=program, db=db)
    except HTTPException as http_e:
        # If the service layer raised an HTTPException, re-raise it
        raise http_e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for getting all Programs
@router_prog.get("", response_model=PaginatedProgramRead)
def get_all_programs(
    db: DBSessionDep,
    page: int = Query(1, description="Page number", ge=1),
    per_page: int = Query(10, description="Items per page", ge=1, le=100)
) -> PaginatedProgramRead:
    """
    Get All Programs

    (Args):
        db: AsyncSession: Database session DI(Injected by FastAPI)
        page: int: Page number for pagination
        per_page: int: Items per page for pagination

    (Returns):
        list[ProgramRead]: List of all Programs (Id and timestamps included)
    """
    try:
        # Calculate the offset to skip the appropriate number of items
        offset = (page - 1) * per_page
        all_records = program_crud.get_all_programs_db(db=db, offset=offset, per_page=per_page)
        count_recs = program_crud.count_records(db=db)

        # Calculate next and previous page URLs
        next_page = f"?page={page + 1}&per_page={per_page}" if len(all_records) == per_page else None
        previous_page = f"?page={page - 1}&per_page={per_page}" if page > 1 else None

        # Return data in paginated format
        # paginated_data = {"count": count_recs, "next": next_page, "previous": previous_page, "all_records": all_records}
        paginated_data = PaginatedProgramRead(count=count_recs, next=next_page, previous=previous_page, all_records=all_records)

        return paginated_data
    
      
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for getting a Program by ID
@router_prog.get("/{program_id}", response_model=ProgramRead)
def get_program_by_id(program_id: int, db: DBSessionDep) -> ProgramRead:
    """
    Get a Program by ID
    Args:
    program_id: int: ID of the Program to retrieve
    db: AsyncSession: Database session DI(Injected by FastAPI)
    Returns:
    Program: Program that was retrieved
    """
    try:
        program = program_crud.get_program_by_id_db(program_id=program_id, db=db)
        if program is None:
            raise HTTPException(status_code=404, detail="Program not found")
        return program
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for updating a Program by ID
@router_prog.patch("/{program_id}", response_model=ProgramRead)
def update_program_by_id(
    program_id: int, program: ProgramUpdate, db: DBSessionDep
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
        return program_crud.update_program_db(
            program_id=program_id, program=program, db=db
        )
    except HTTPException as http_e:
        # If the service layer raised an HTTPException, re-raise it
        raise http_e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_prog.delete("/{program_id}")
def delete_program_by_id(program_id: int, db: DBSessionDep):
    """
    Delete a Program by ID
    Args:
        program_id: int: ID of the Program to delete
        db: AsyncSession: Database session
    Returns:
        Program: Program that was deleted
    """
    return program_crud.delete_program_db(program_id=program_id, db=db)