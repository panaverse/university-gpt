
from app.data.common import Base, UserType
from typing import List
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, Boolean, Enum, UUID
import uuid


class MixinUsers:
    """
    MixinUsers model represents a user in the system. It contains
    common fields that are shared by all types of users will not be a table in DB.
    """

    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    verified_email: Mapped[bool] = mapped_column(Boolean, default=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    father_name: Mapped[str] = mapped_column(String, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=True)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), nullable=True)
    profile_picture: Mapped[str] = mapped_column(String, nullable=True)

    def get_fullname(self) -> str:
        """
        Compute and return the full name of the user.
        """
        return f"{self.first_name} {self.last_name}"


class Qualification(Base):
    """
    Qualification model represents a qualification that a user can have.
    It contains fields like qualification_id, qualification_name,
    qualification_start_date, qualification_end_date, and qualification_institute.
    """

    __tablename__ = "qualifications"
    qualification_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    qualification_name: Mapped[str] = mapped_column(String, nullable=False)
    qualification_start_date: Mapped[str] = mapped_column(
        String, nullable=False)
    qualification_end_date: Mapped[str] = mapped_column(String, nullable=False)
    qualification_institute: Mapped[str] = mapped_column(
        String, nullable=False)


class Interest(Base):
    """
    Interest model represents an interest that a user can have.
    It contains fields like interest_id and interest_name.
    """

    __tablename__ = "interests"
    interest_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    interest_name: Mapped[str] = mapped_column(String, nullable=False)

    # Join table for Instructor and Course (one instructor can teach many courses
    # and one course can be taught by many instructors)


class Instructor(Base, MixinUsers):
    """
    Instructor model represents an instructor in the system.
    It inherits from the MixinUsers model and adds additional fields
    specific to instructors like id, instructor_code,
    instructor_qualifications, and instructor_courses.
    """

    __tablename__ = "instructors"
    instructor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # TODO: What is "instructor_code" in INSTRUCTOR table.
    instructor_code: Mapped[str] = mapped_column(String, nullable=True)
    # an instructor has many qualifications
    instructor_qualifications: Mapped[list["Qualification"]] = relationship(
        "Qualification", back_populates="instructor"
    )  # TODO: If we back populate it creates bidirectional relationship. We shall del it or define it in Qualification modal.
    # instructor can teach many courses
    instructor_courses: Mapped[list["InstructorCourse"]] = relationship(
        "InstructorCourse", back_populates="instructor"
    )


class Student(Base, MixinUsers):
    """
    Student model represents a student in the system.
    It inherits from the MixinUsers model and adds additional
    fields specific to students like student_id, student_roll_number,
    student_qualifications, student_interests, and program_id.
    """

    __tablename__ = "students"
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    student_roll_number: Mapped[str] = mapped_column(String, nullable=True)
    student_qualifications: Mapped[List["Qualification"]] = relationship(
        "Qualification", back_populates="student"
    )
    student_interests: Mapped[List["Interest"]] = relationship(
        "Interest", back_populates="student"
    )
    # student enrollment ins program
    # : Mapped["app.data.university.Program"] 
    program_id= mapped_column(
        ForeignKey("programs.program_id"), nullable=True
    )
    # a program can have many students
    # (one-to-many relationship with Program model)
    program = relationship(
        "app.data.university.Program", back_populates="students")

    # A one-to-many relationship with the QuizAnswerSheet class, meaning a single student can have multiple quiz answer sheets, each representing an attempt at a quiz.
    # This is the back_populates part for the student_id foreign key in the QuizAnswerSheet class.
    quiz_answer_sheets: Mapped[list["app.data.quiz.QuizAnswerSheet"]] = relationship(
        "QuizAnswerSheet",
        back_populates="student",
        cascade="all, delete-orphan"
    )


class InstructorCourse(Base):
    """
    InstructorCourse model represents the relationship between
    instructors and courses. Each row represents an instructor
    teaching a course.
    """

    __tablename__ = "instructor_courses"
    instructor_course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    instructor_id: Mapped["Instructor"] = mapped_column(
        ForeignKey("instructors.instructor_id"), nullable=False
    )
    # an instructor can teach list of courses
    # (one-to-many relationship with Instructor model)
    course: Mapped[list["app.data.university.Course"]] = relationship(
        "app.data.university.Course", back_populates="instructor_courses"
    )
