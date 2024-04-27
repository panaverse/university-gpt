from fastapi import HTTPException
from sqlmodel import Session
import random
import pytest

from tests.utils.test_items import test_program_data
from app.crud.program_crud import program_crud
from app.crud.university_crud import university_crud
from app.models.program_models import ProgramCreate, ProgramUpdate, Program, ProgramRead

# fixture that get all universities and return the first one is
@pytest.fixture
def university_id(db: Session):
    all_universities = university_crud.get_all_universities_db(db=db, offset=0, per_page=10)
    return all_universities[0].id

# Create and return a program
@pytest.fixture
def program_id(db: Session, university_id):
    program_name = test_program_data.get("name") + str(random.randint(1, 10000))
    program = ProgramCreate(name=program_name, university_id=university_id)
    created_program = program_crud.create_program_db(program=program, db=db)
    return created_program.id

def test_create_program_db(db: Session, university_id):
    program_name = test_program_data.get("name") + str(random.randint(1, 10000))
    program = ProgramCreate(name=program_name, university_id=university_id)
    created_program = program_crud.create_program_db(program=program, db=db)
    
    assert created_program.name == program.name
    assert created_program.description is None
    assert created_program.id is not None

def test_get_all_programs_db(db: Session):
    all_programs = program_crud.get_all_programs_db(db=db, offset=0, per_page=10)
    assert all_programs is not None
    assert len(all_programs) > 0

def test_get_program_by_id_db(db: Session):
    all_programs = program_crud.get_all_programs_db(db=db, offset=0, per_page=10)
    assert all_programs is not None
    assert len(all_programs) > 0
    program_id = all_programs[0].id
    program = program_crud.get_program_by_id_db(program_id=program_id, db=db)
    assert program is not None
    assert program.id == program_id

def test_update_program_by_id_db(db: Session):
    all_programs = program_crud.get_all_programs_db(db=db, offset=0, per_page=10)
    assert all_programs is not None
    assert len(all_programs) > 0
    program_id = all_programs[0].id
    program_name = test_program_data.get("name") + str(random.randint(1, 10000))
    program = ProgramUpdate(name=program_name)
    updated_program = program_crud.update_program_db(program_id=program_id, program=program, db=db)
    assert updated_program is not None
    assert updated_program.id == program_id
    assert updated_program.name == program_name

def test_delete_program_by_id_db(db: Session, program_id):

        program = program_crud.delete_program_db(program_id=program_id, db=db)
        assert program == {"message": "Program deleted"}
    
        # Raise HttpException with 404 status code Check if the program is deleted
        with pytest.raises(HTTPException) as e:
            program_crud.get_program_by_id_db(program_id=program_id, db=db)

# # # Create program duplicate  
def test_create_program_duplicate(db: Session):
    program_name = test_program_data.get("name")
    program = ProgramCreate(name=program_name, university_id=1)
    with pytest.raises(HTTPException) as e:
        program_crud.create_program_db(program=program, db=db)
        assert e.status_code == 400
        assert e.detail == "Program with same name already exists"

# # # Create program with invalid university_id
def test_create_program_invalid_university_id(db: Session):
    program = ProgramCreate(name=test_program_data.get("name"), university_id=100)
    with pytest.raises(HTTPException) as e:
        program_crud.create_program_db(program=program, db=db)
        assert e.status_code == 400
        assert e.detail == "Offset cannot be negative"
    
# # # Test offset in get_all_programs_db
def test_get_all_programs_offset(db: Session):
    with pytest.raises(HTTPException) as e:

        program_crud.get_all_programs_db(db=db, offset=1, per_page=0)
        assert e.status_code == 400
        assert e.detail == "Per page items cannot be less than 1"


# # twsr get_program with inva;id
def test_get_program_by_id_invalid(db: Session):
    with pytest.raises(HTTPException) as e:
        program_crud.get_program_by_id_db(program_id=100, db=db)
        assert e.status_code == 404
        assert e.detail == "Program not found"


# # # update program with invalid id
def test_update_program_invalid_id(db: Session):
    program = ProgramUpdate(name=test_program_data.get("name"))
    with pytest.raises(HTTPException) as e:
        program_crud.update_program_db(program_id=100, program=program, db=db)
        assert e.status_code == 404
        assert e.detail == "Program not found"

# # # delete program with invalid id
def test_delete_program_invalid_id(db: Session):
    with pytest.raises(HTTPException) as e:
        program_crud.delete_program_db(program_id=100, db=db)
        assert e.status_code == 404
        assert e.detail == "Program not found"