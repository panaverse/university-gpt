from fastapi import HTTPException
from sqlmodel import Session
import random
import pytest
from tests.utils.test_items import test_course_data
from app.crud.course_crud import course_crud
from app.crud.program_crud import program_crud
from app.crud.university_crud import university_crud
from app.models.program_models import Program
from app.models.course_models import CourseCreate, CourseUpdate, Course, CourseRead

# fixture that gets all programs and returns the first one
@pytest.fixture(autouse=True)
def program_id(db: Session):
    all_universities = university_crud.get_all_universities_db(db=db, offset=0, per_page=10)
    university_id= all_universities[0].id
    # Create a program
    program_name = test_course_data.get("name") + str(random.randint(1, 10000))
    program = Program(name=program_name, university_id=university_id)

    created_program = program_crud.create_program_db(program=program, db=db)
    return created_program.id

# Create and return a course
@pytest.fixture
def course_id(db: Session, program_id):
    course_name = test_course_data.get("name") + str(random.randint(1, 10000))
    course = CourseCreate(name=course_name, program_id=program_id)
    created_course = course_crud.create_course_db(course=course, db=db)
    return created_course.id

def test_create_course_db(db: Session, program_id):
    course_name = test_course_data.get("name") + str(random.randint(1, 10000))
    course = CourseCreate(name=course_name, program_id=program_id)
    created_course = course_crud.create_course_db(course=course, db=db)
    
    assert created_course.name ==  course_name
    assert created_course.description is None
    assert created_course.id is not None

def test_get_all_courses_db(db: Session):
    all_courses = course_crud.get_all_courses_db(db=db, offset=0, per_page=10)
    assert all_courses is not None
    assert len(all_courses) > 0

def test_get_course_by_id_db(db: Session, course_id):
    course = course_crud.get_course_by_id_db(course_id=course_id, db=db)
    assert course is not None
    assert course.id == course_id

def test_update_course_by_id_db(db: Session, course_id):

    course_name = test_course_data.get("name") + str(random.randint(1, 10000))
    course = CourseUpdate(name=course_name)
    updated_course = course_crud.update_course_db(course_id=course_id, course=course, db=db)
    assert updated_course is not None
    assert updated_course.id == course_id
    assert updated_course.name == course_name

def test_delete_course_by_id_db(db: Session, course_id):
    course = course_crud.delete_course_db(course_id=course_id, db=db)
    assert course == {"message": "Course deleted"}
    
    # Raise HttpException with 404 status code Check if the course is deleted
    with pytest.raises(HTTPException) as e:
        course_crud.get_course_by_id_db(course_id=course_id, db=db)

# # # # Create course with invalid program_id
def test_create_course_invalid_program_id(db: Session):
    course = CourseCreate(name=test_course_data.get("name"), program_id=100)
    with pytest.raises(HTTPException) as e:
        course_crud.create_course_db(course=course, db=db)
        assert e.status_code == 400
        assert e.detail == "Invalid program ID"
    
# # # Test offset in get_all_courses_db
def test_get_all_courses_offset(db: Session):
    with pytest.raises(HTTPException) as e:
        course_crud.get_all_courses_db(db=db, offset=1, per_page=0)
        assert e.status_code == 400
        assert e.detail == "Per page items cannot be less than 1"

# # # Get course with invalid id
def test_get_course_by_id_invalid(db: Session):
    with pytest.raises(HTTPException) as e:
        course_crud.get_course_by_id_db(course_id=100, db=db)
        assert e.status_code == 404
        assert e.detail == "Course not found"

# # # Update course with invalid id
def test_update_course_invalid_id(db: Session):
    course = CourseUpdate(name=test_course_data.get("name"))
    with pytest.raises(HTTPException) as e:
        course_crud.update_course_db(course_id=100, course=course, db=db)
        assert e.status_code == 404
        assert e.detail == "Course not found"

# # # Delete course with invalid id
def test_delete_course_invalid_id(db: Session):
    with pytest.raises(HTTPException) as e:
        course_crud.delete_course_db(course_id=10000, db=db)
        assert e.status_code == 404
        assert e.detail == "Course not found"
