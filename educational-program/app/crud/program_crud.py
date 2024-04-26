from fastapi import HTTPException
from sqlmodel import select, Session

from app.models.program_models import Program, ProgramCreate, ProgramUpdate

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
        obj_in = Program.model_validate(program)
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    # Get all Programs
    def get_all_programs_db(self, *, db: Session, offset: int, limit: int):
        """
        Get All Programs
        Args:
        db: Session: Database session
        Returns:
        list[ProgramRead]: List of all Programs (Id and timestamps included)
        """
        stmt = select(Program).offset(offset).limit(limit)
        programs_req = db.exec(stmt)
        programs = programs_req.all()
        return programs

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
        program = db.get(Program, program_id)
        return program

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
        db_program = db.get(Program, program_id)
        if not db_program:
            raise HTTPException(status_code=404, detail="Program not found")

        program_data = program.model_dump(exclude_unset=True)
        db_program.sqlmodel_update(program_data)
        db.add(db_program)

        db.commit()
        db.refresh(db_program)

        return db_program

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
        program = db.get(Program, program_id)
        if program is None:
            raise HTTPException(status_code=404, detail="Program not found")
        db.delete(program)
        db.commit()
        # return program
        return {"message": "Program deleted"}

program_crud = ProgramCRUD()
