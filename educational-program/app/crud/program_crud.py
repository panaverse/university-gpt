from fastapi import HTTPException
from sqlmodel import select, Session

from app.models.program_models import Program, ProgramCreate, ProgramUpdate
from app.models.university_models import University

class ProgramCRUD:
    def create_program_db(self, *, program: ProgramCreate, db: Session):
        """
        Create a new Program in the database
        Args:
            program: ProgramCreate: New Program to create (from request body)
            db: Session: Database session
        Returns:
            Program: Program that was created (with Id and timestamps included)
        """
        # Check if Program for Same Same Exists
        try:
            program_exists = db.exec(select(Program).where(Program.name == program.name)).first()
            if program_exists:
                raise HTTPException(status_code=400, detail="Program with same name already exists")

            # Check if University Exists
            university_exists = db.get(University, program.university_id)
            if not university_exists:
                raise HTTPException(status_code=404, detail="University not found")
            obj_in = Program.model_validate(program)
            db.add(obj_in)
            db.commit()
            db.refresh(obj_in)
            return obj_in
        except HTTPException as http_e:
            db.rollback()
            # If the service layer raised an HTTPException, re-raise it
            raise http_e
        except Exception as e:
            db.rollback()
            # Handle specific exceptions with different HTTP status codes if needed
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    # Get all Programs
    def get_all_programs_db(self, *, db: Session, offset: int, per_page: int):
        """
        Get All Programs
        Args:
        db: Session: Database session
        Returns:
        list[ProgramRead]: List of all Programs (Id and timestamps included)
        """
        try:
            if offset < 0:
                raise HTTPException(status_code=400, detail="Offset cannot be negative")
            if per_page < 1:
                raise HTTPException(status_code=400, detail="Per page items cannot be less than 1")
            
            programs = db.exec(select(Program).offset(offset).limit(per_page)).all()
            if programs is None:
                raise HTTPException(status_code=404, detail="Programs not found")
            return programs
        except HTTPException as http_e:
            db.rollback()
            # If the service layer raised an HTTPException, re-raise it
            raise http_e
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    # Get Program by ID
    def get_program_by_id_db(self, *, program_id: int, db: Session):
        """
        Get a Program by ID
        Args:
            program_id: int: ID of the Program to retrieve
            db: Session: Database session
        Returns:
            Program: Program that was retrieved
        """
        try:
            program = db.get(Program, program_id)
            if program is None:
                raise HTTPException(status_code=404, detail="Program not found")
            return program
        except HTTPException as http_e:
            db.rollback()
            # If the service layer raised an HTTPException, re-raise it
            raise http_e
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    # Update Program by ID
    def update_program_db(
        self, *, program_id: int, program: ProgramUpdate, db: Session
    ):
        """
        Update a Program by ID
        Args:
            program_id: int: ID of the Program to update
            program: ProgramUpdate: New values for Program
            db: Session: Database session
        Returns:
            Program: Program that was updated (with Id and timestamps included)
        """
        try:
            db_program = db.get(Program, program_id)
            if not db_program:
                raise HTTPException(status_code=404, detail="Program not found")
            
            # If Program is Trying to change name
            if program.name:
                program_exists = db.exec(select(Program).where(Program.name == program.name)).first()
                if program_exists:
                    raise HTTPException(status_code=400, detail="Program with same name already exists")
                
            # If Program is Trying to change university_id
            if program.university_id:
                university_exists = db.get(University, program.university_id)
                if not university_exists:
                    raise HTTPException(status_code=404, detail=f"University with id {program.university_id} not found")
            
            program_data = program.model_dump(exclude_unset=True)
            db_program.sqlmodel_update(program_data)
            db.add(db_program)

            db.commit()
            db.refresh(db_program)

            return db_program
        except HTTPException as http_e:
            db.rollback()
            # If the service layer raised an HTTPException, re-raise it
            raise http_e
        except Exception as e:
            db.rollback()
            # Handle specific exceptions with different HTTP status codes if needed
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    # Delete Program by ID
    def delete_program_db(self, *, program_id: int, db: Session):
        """
        Delete a Program by ID
        Args:
            program_id: int: ID of the Program to delete
            db: Session: Database session
        Returns:
            Program: Program that was deleted
        """
        try:
            program = db.get(Program, program_id)
            if program is None:
                raise HTTPException(status_code=404, detail="Program not found")
            db.delete(program)
            db.commit()
            # return program
            return {"message": "Program deleted"}
        except HTTPException as http_e:
            db.rollback()
            # If the service layer raised an HTTPException, re-raise it
            raise http_e
        except Exception as e:
            db.rollback()
            # Handle specific exceptions with different HTTP status codes if needed
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    def count_records(self, *, db: Session) -> int:
        try:
            query = select(Program.name)
            items = db.exec(query).all()
            count = len(items)
            return count
        except Exception as e:
            db.rollback()
            # Log the exception for debugging purposes
            print(f"Error counting SearchToolRecord items: {e}")
            # Re-raise the exception to be handled at the endpoint level
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


program_crud = ProgramCRUD()
