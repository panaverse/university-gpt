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
        obj_in = University.model_validate(university)
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def get_all_universities_db(
        self, *, db: Session, offset: int, limit: int
    ):
        """
        Get All Universities
        Args:
        db: Session: Database session
        Returns:
            University: List of all Universities (Id and timestamps included)
        """
        universities = db.exec(select(University).offset(offset).limit(limit))
        print(universities)
        all_universities = universities.all()
        if all_universities is None:
            raise HTTPException(status_code=404, detail="Universities not found")
        return all_universities

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


university_crud = UniversityCRUD()

