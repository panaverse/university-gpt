from fastapi import HTTPException
from sqlmodel import Session
import random
import pytest

from app.crud.university_crud import university_crud
from app.models.university_models import UniversityCreate, UniversityUpdate, University, UniversityRead
from tests.utils.test_items import test_uni_data


def test_create_university_db(db: Session):
    uni_name = test_uni_data.get("name") + str(random.randint(1, 10000))

    university = UniversityCreate(name=uni_name)
    created_university = university_crud.create_university_db(university=university, db=db)
    assert created_university.name == university.name
    assert created_university.description is None
    assert created_university.id is not None


def test_get_all_universities_db(db: Session):
    all_universities = university_crud.get_all_universities_db(db=db, offset=0, per_page=10)
    assert all_universities is not None
    assert len(all_universities) > 0

def test_get_university_by_id_db(db: Session):
    all_universities = university_crud.get_all_universities_db(db=db, offset=0, per_page=10)
    assert all_universities is not None
    assert len(all_universities) > 0
    uni_id = all_universities[0].id
    university = university_crud.get_university_by_id_db(university_id=uni_id, db=db)
    assert university is not None
    assert university.id == uni_id

def test_update_university_by_id_db(db: Session):
    all_universities = university_crud.get_all_universities_db(db=db, offset=0, per_page=10)
    assert all_universities is not None
    assert len(all_universities) > 0
    uni_id = all_universities[0].id
    uni_name = test_uni_data.get("name") + str(random.randint(1, 10000))
    university = UniversityUpdate(name=uni_name)
    updated_university = university_crud.update_university_db(university_id=uni_id, university=university, db=db)
    assert updated_university is not None
    assert updated_university.id == uni_id
    assert updated_university.name == uni_name

def test_delete_university_by_id_db(db: Session):

    all_universities = university_crud.get_all_universities_db(db=db, offset=0, per_page=10)
    assert all_universities is not None
    assert len(all_universities) > 0
    uni_id = all_universities[0].id
    university = university_crud.delete_university_db(university_id=uni_id, db=db)
    assert university == {"message": "University deleted"}

    # Raise HttpException with 404 status code Check if the university is deleted
    with pytest.raises(HTTPException) as e:
        university_crud.get_university_by_id_db(university_id=uni_id, db=db)

# Create uni duplicate
def test_create_university_duplicate(db: Session):
    uni_name = test_uni_data.get("name") + str(random.randint(1, 10000))

    university = UniversityCreate(name=uni_name)
    created_university = university_crud.create_university_db(university=university, db=db)
    assert created_university.name == university.name
    assert created_university.description is None
    assert created_university.id is not None

    # Create duplicate
    with pytest.raises(HTTPException) as e:
        university_crud.create_university_db(university=university, db=db)
        assert e.status_code == 400
        assert e.detail == "University with same name already exists"

# Test offset in get_all_universities_db
def test_get_all_universities_db_offset(db: Session):
   
   with pytest.raises(HTTPException) as e:
       university_crud.get_all_universities_db(db=db, offset=-1, per_page=10)
       assert e.status_code == 400
       assert e.detail == "Offset cannot be negative"

# Test per_page in get_all_universities_db
def test_get_all_universities_db_per_page(db: Session):
   
   with pytest.raises(HTTPException) as e:
       university_crud.get_all_universities_db(db=db, offset=0, per_page=0)
       assert e.status_code == 400
       assert e.detail == "Per page items cannot be less than 1"

# twsr get_university_by_id_db inva;id
def test_get_university_invalid_id(db: Session):
    with pytest.raises(HTTPException) as e:
        university_crud.get_university_by_id_db(university_id=100, db=db)
        assert e.status_code == 404
        assert e.detail == "University not found"

# Test update_university_by_id_db invalid id
def test_update_university_invalid_id(db: Session):
    university = UniversityUpdate(name="University of Temp Test")
    with pytest.raises(HTTPException) as e:
        university_crud.update_university_db(university_id=100, university=university, db=db)
        assert e.status_code == 404
        assert e.detail == "University not found"

# Test delete_university_by_id_db invalid id
def test_delete_university_invalid_id(db: Session):
    with pytest.raises(HTTPException) as e:
        university_crud.delete_university_db(university_id=100, db=db)
        assert e.status_code == 404
        assert e.detail == "University not found"