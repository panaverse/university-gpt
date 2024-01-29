from app.data.common import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, UUID
import uuid


class University(Base):
    """
    University model represents a university in the system. It contains fields like university_id, university_name, and university_description. It also has a one-to-many relationship with the Program model, meaning a university can have many programs.
    """

    __tablename__ = "universities"
    university_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    university_name: Mapped[str] = mapped_column(String, nullable=False)
    university_description: Mapped[str] = mapped_column(String, nullable=True)
    # a university can have many programs (one-to-many relationship with Program model)
    programs: Mapped[list["Program"]] = relationship(
        "Program", back_populates="university"
    )


class Program(Base):
    """
    Program model represents an educational program in the system. It contains fields like program_id, program_name, and program_description. It also has a one-to-many relationship with the Course and Student models, meaning a program can have many courses and students.
    """

    __tablename__ = "programs"
    program_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    program_name: Mapped[str] = mapped_column(String, nullable=False)
    program_description: Mapped[str] = mapped_column(String, nullable=True)
    # a program can have many courses (one-to-many relationship with Course model)
    course: Mapped[list["Course"]] = relationship(
        "Course", back_populates="program")
    # a program can have many students (one-to-many relationship with Student model)
    students: Mapped[list["app.data.user.Student"]] = relationship(
        "Student", back_populates="program"
    )

    skill: Mapped[list["Skill"]] = relationship(
        "Skill", back_populates="program")


class Skill(Base):
    """
    Each Program can have many Skills, and each Skill is associated with one Program.
    """
    __tablename__ = "skills"
    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_name: Mapped[str] = mapped_column(String, nullable=False)
    skill_description: Mapped[str] = mapped_column(String, nullable=True)

    # a program can have many skills (one-to-many relationship with Skill model)
    program_id: Mapped["Program"] = mapped_column(
        ForeignKey("programs.program_id"), nullable=True)
    program: Mapped["Program"] = relationship(
        "Program", back_populates="skill")


class Course(Base):
    """
    Course model represents a course in the system. It contains fields like course_name and course_description. It also has a many-to-one relationship with the Program model, meaning a course is a part of a program. Additionally, it has a one-to-many relationship with the Topic and InstructorCourse models, meaning a course can have many topics and can be taught by many instructors.
    """

    __tablename__ = "courses"
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    course_name: Mapped[str] = mapped_column(String, nullable=False)
    course_description: Mapped[str] = mapped_column(String, nullable=True)
    program_id: Mapped["Program"] = mapped_column(
        ForeignKey("programs.program_id"), nullable=True)
    # course is a part of program (many-to-one relationship with Program model)
    program: Mapped["Program"] = relationship(
        "Program", back_populates="courses")
    # course can have many topics (one-to-many relationship with Topic model)
    topics: Mapped[list["app.data.topic.Topic"]] = relationship(
        "Topic", back_populates="course")
    # course can be taught by many instructors (one-to-many relationship with InstructorCourse model)
    instructor_courses: Mapped[list["app.data.user.InstructorCourse"]] = relationship(
        "app.data.user.InstructorCourse", back_populates="course"
    )
