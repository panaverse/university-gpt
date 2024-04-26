from fastapi import APIRouter, Query, HTTPException

from app.models.program_models import ProgramCreate, ProgramRead, ProgramUpdate
from app.api.deps import DBSessionDep
from app.crud.program_crud import program_crud

router_prog = APIRouter()


# Endpoints for creating a new Program
@router_prog.post("", response_model=ProgramRead)
async def create_new_program(
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
        return await program_crud.create_program_db(program=program, db=db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints for getting all Programs
@router_prog.get("", response_model=list[ProgramRead])
async def get_all_programs(
    db: DBSessionDep,
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
async def get_program_by_id(program_id: int, db: DBSessionDep) -> ProgramRead:
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
        return await program_crud.update_program_db(
            program_id=program_id, program=program, db=db
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_prog.delete("/{program_id}")
async def delete_program_by_id(program_id: int, db: DBSessionDep):
    """
    Delete a Program by ID
    Args:
        program_id: int: ID of the Program to delete
        db: AsyncSession: Database session
    Returns:
        Program: Program that was deleted
    """
    return await program_crud.delete_program_db(program_id=program_id, db=db)