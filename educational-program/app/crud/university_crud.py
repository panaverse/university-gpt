from fastapi import HTTPException
from sqlmodel import select, Session

from app.models.university_models import University, UniversityCreate, UniversityUpdate


class UniversityCRUD:
    def create_university_db(
        self, *, university: UniversityCreate, db: Session
    ):
        """
        Create a new University in the database
        Args:
            university: UniversityCreate: New University to create (from request body)
            db: Session: Database session
        Returns:
            University: University that was created (with Id and timestamps included)
        """
        # Check if University with Same name already exists
        university_exists = db.exec(select(University).where(University.name == university.name)).first()
        if university_exists:
            raise HTTPException(status_code=400, detail="University with same name already exists")
        obj_in = University.model_validate(university)
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def get_all_universities_db(
        self, *, db: Session, offset: int, per_page: int
    ):
        """
        Get All Universities
        Args:
        db: Session: Database session
        Returns:
            University: List of all Universities (Id and timestamps included)
        """
        universities = db.exec(select(University).offset(offset).limit(per_page)).all()
        if universities is None:
            raise HTTPException(status_code=404, detail="Universities not found")
        return universities

    def get_university_by_id_db(self, *, university_id: int, db: Session):
        """
        Get a University by ID
        Args:
            university_id: int: ID of the University to retrieve
            db: Session: Database session
        Returns:
            University: University that was retrieved
        """
        university = db.get(University, university_id)
        if university is None:
            raise HTTPException(status_code=404, detail="University not found")
        return university

    def update_university_db(
        self, *, university_id: int, university: UniversityUpdate, db: Session
    ):
        """
        Update a University by ID
        Args:
            university_id: int: ID of the University to update
            university: UniversityUpdate: New values for University
            db: Session: Database session
        Returns:
            University: University that was updated (with Id and timestamps included)
        """
        db_university = db.get(University, university_id)
        if not db_university:
            raise HTTPException(status_code=404, detail="university not found")
        university_data = university.model_dump(exclude_unset=True)
        db_university.sqlmodel_update(university_data)
        print(university_data)
        db.add(db_university)

        db.commit()
        db.refresh(db_university)
        return db_university

    def delete_university_db(self, *, university_id: int, db: Session):
        """
        Delete a University by ID
        Args:
            university_id: int: ID of the University to delete
            db: Session: Database session
        Returns:
            University: University that was deleted
        """
        university = db.get(University, university_id)
        if university is None:
            raise HTTPException(status_code=404, detail="University not found")
        db.delete(university)
        db.commit()
        # return university
        return {"message": "University deleted"}

    def count_records(self, *, db: Session) -> int:
        try:
            query = select(University.name)
            items = db.exec(query).all()
            count = len(items)
            return count
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error counting SearchToolRecord items: {e}")
            # Re-raise the exception to be handled at the endpoint level
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

university_crud = UniversityCRUD()

