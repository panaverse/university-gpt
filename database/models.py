from common import Base, UserType, QuestionType
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
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    father_name: Mapped[str] = mapped_column(String, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=True)
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
    qualification_start_date: Mapped[str] = mapped_column(String, nullable=False)
    qualification_end_date: Mapped[str] = mapped_column(String, nullable=False)
    qualification_institute: Mapped[str] = mapped_column(String, nullable=False)


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
    instructor_code: Mapped[str] = mapped_column(String, nullable=True)
    # an instructor has many qualifications
    instructor_qualifications: Mapped[List["Qualification"]] = relationship(
        "Qualification", back_populates="instructor"
    )
    # instructor can teach many courses
    instructor_courses: Mapped[List["InstructorCourse"]] = relationship(
        "InstructorCourse", back_populates="instructor"
    )

    # Join table for Instructor and Course (one instructor can teach many courses
    # and one course can be taught by many instructors)


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
    course: Mapped[List["Course"]] = relationship(
        "Course", back_populates="instructor_courses"
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
    course: Mapped[List["Course"]] = relationship("Course", back_populates="program")
    # a program can have many students (one-to-many relationship with Student model)
    students: Mapped[List["Student"]] = relationship(
        "Student", back_populates="program"
    )

    # program_code: Mapped[str] = mapped_column(String, nullable=False)
    # program_duration: Mapped[int] = mapped_column(String, nullable=False)
    # program_duration_unit: Mapped[str] = mapped_column(String, nullable=False)
    # program_start_date: Mapped[str] = mapped_column(String, nullable=False)
    # program_end_date: Mapped[str] = mapped_column(String, nullable=False)
    # program_fee: Mapped[int] = mapped_column(String, nullable=False)
    # program_fee_currency: Mapped[str] = mapped_column(String, nullable=False)


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
    program_id: Mapped["Program"] = mapped_column(
        ForeignKey("programs.program_id"), nullable=True
    )
    # a program can have many students
    # (one-to-many relationship with Program model)
    program: Mapped["Program"] = relationship("Program", back_populates="students")


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
    programs: Mapped[List["Program"]] = relationship(
        "Program", back_populates="university"
    )


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
        ForeignKey("programs.program_id"), nullable=True
    )
    # course is a part of program (many-to-one relationship with Program model)
    program: Mapped["Program"] = relationship("Program", back_populates="courses")
    # course can have many topics (one-to-many relationship with Topic model)
    topics: Mapped[List["Topic"]] = relationship("Topic", back_populates="course")
    # course can be taught by many instructors (one-to-many relationship with InstructorCourse model)
    instructor_courses: Mapped[List["InstructorCourse"]] = relationship(
        "InstructorCourse", back_populates="course"
    )

    # course_code: Mapped[str] = mapped_column(String, nullable=False)
    # course_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    # course_duration_unit: Mapped[str] = mapped_column(String, nullable=False)
    # course_start_date: Mapped[str] = mapped_column(String, nullable=False)


class Topic(Base):
    """
    Topic model represents a topic in the system. It contains fields like topic_id, title, and description. It also has a self-referential relationship, meaning a topic can have subtopics (children_topic) and a parent topic (parent_topic). Additionally, it has a one-to-many relationship with the Question model, meaning a topic can have many questions associated with it.
    """

    __tablename__ = "topics"
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    topic_name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    course_id:Mapped["Course"] = mapped_column(
        ForeignKey("courses.course_id"), nullable=True
    )
    course: Mapped["Course"] = relationship("Course", back_populates="topics")

    parent_topic_id: Mapped[UUID] = mapped_column(
        ForeignKey("topics.topic_id"), nullable=True
    )
    # self referential relationship
    children_topic = relationship("Topic", back_populates="parent_topic")
    parent_topic = relationship(
        "Topic", back_populates="children_topic", remote_side=[topic_id]
    )


class Quiz(Base):
    """
    Quiz model represents a quiz in the system. It contains fields like quiz_name and quiz_description. It also has a many-to-one relationship with the Topic model, meaning a quiz is associated with a topic. Additionally, it has a one-to-many relationship with the Question model, meaning a quiz can have many questions associated with it.
    """

    __tablename__ = "quizzes"
    quiz_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    quiz_name: Mapped[str] = mapped_column(String, nullable=False)
    quiz_description: Mapped[str] = mapped_column(String, nullable=True)
    quiz_topic_id: Mapped["Topic"] = mapped_column(
        ForeignKey("topics.topic_id"), nullable=True
    )
    quiz_topic: Mapped["Topic"] = relationship("Topic", back_populates="quizzes")
    questions: Mapped[List["Question"]] = relationship(
        "Question", back_populates="quiz"
    )


class Question(Base):
    """
    Question model represents a question in the system. It contains fields like question_text, question_type, question_options, question_answer, question_explanation, and question_difficulty. It also has a many-to-one relationship with the Topic model, meaning a question is associated with a topic.
    """

    __tablename__ = "questions"
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    question_text: Mapped[str] = mapped_column(String, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType), nullable=False
    )
    question_points: Mapped[int] = mapped_column(String, nullable=False)
    question_quiz_id: Mapped["Quiz"] = mapped_column(
        ForeignKey("quizzes.quiz_id"), nullable=True
    )
    question_quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions")


class Option(Base):
    """
    Option model represents an option for a question in the system. It contains fields like option_text and option_is_correct. It also has a many-to-one relationship with the Question model, meaning an option is associated with a question.
    """

    __tablename__ = "options"
    option_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    option_text: Mapped[str] = mapped_column(String, nullable=False)
    option_is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    option_question_id: Mapped["Question"] = mapped_column(
        ForeignKey("questions.question_id"), nullable=True
    )
    option_question: Mapped["Question"] = relationship(
        "Question", back_populates="options"
    )


class FreeTextQuestions(Base):
    __tablename__ = "free_text_questions"
    free_text_question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    free_text_question_text: Mapped[str] = mapped_column(String, nullable=False)
    question_id: Mapped["Question"] = mapped_column(
        ForeignKey("questions.question_id"), nullable=True
    )
    free_text_question: Mapped["Question"] = relationship(
        "Question", back_populates="free_text_questions"
    )


class AnswerSheet(Base):
    """
    AnswerSheet model represents a student's answer sheet in the system. It contains fields like answer_sheet_id, question_id, and student_id. It also has a many-to-one relationship with the Question and Student models, meaning an answer sheet is associated with a question and a student.
    """

    __tablename__ = "answer_sheets"
    answer_sheet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    question_id: Mapped["Question"] = mapped_column(
        ForeignKey("questions.question_id"), nullable=True
    )
    student_id: Mapped["Student"] = mapped_column(
        ForeignKey("students.student_id"), nullable=True
    )
    question: Mapped["Question"] = relationship(
        "Question", back_populates="answer_sheets"
    )
    student: Mapped["Student"] = relationship("Student", back_populates="answer_sheets")


class OptionAnswerSheet(Base):
    """
    OptionAnswerSheet model represents a student's answer for a multiple-choice question in the system. It contains fields like option_answer_sheet_id, option_id, and answer_sheet_id. It also has a many-to-one relationship with the Option and AnswerSheet models, meaning an option answer sheet is associated with an option and an answer sheet.
    """

    __tablename__ = "option_answer_sheets"
    option_answer_sheet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    option_id: Mapped["Option"] = mapped_column(
        ForeignKey("options.option_id"), nullable=True
    )
    answer_sheet_id: Mapped["AnswerSheet"] = mapped_column(
        ForeignKey("answer_sheets.answer_sheet_id"), nullable=True
    )
    option: Mapped["Option"] = relationship(
        "Option", back_populates="option_answer_sheets"
    )
    answer_sheet: Mapped["AnswerSheet"] = relationship(
        "AnswerSheet", back_populates="option_answer_sheets"
    )


class FreeTextAnswerSheet(Base):
    """
    FreeTextAnswerSheet model represents a student's answer for a free-text question in the system. It contains fields like free_text_answer_sheet_id, free_text_answer, and answer_sheet_id. It also has a many-to-one relationship with the AnswerSheet model, meaning a free-text answer sheet is associated with an answer sheet.
    """

    __tablename__ = "free_text_answer_sheets"
    free_text_answer_sheet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    free_text_answer: Mapped[str] = mapped_column(String, nullable=False)
    answer_sheet_id: Mapped["AnswerSheet"] = mapped_column(
        ForeignKey("answer_sheets.answer_sheet_id"), nullable=True
    )
    answer_sheet: Mapped["AnswerSheet"] = relationship(
        "AnswerSheet", back_populates="free_text_answer_sheets"
    )


# class CaseStudy(Base):
# """
# CaseStudy model represents a case study in the system. It contains the
# text of the case study, the question it belongs to, and whether it is the
# correct answer.
# """

# __tablename__ = "case_studies"
# case_study_text: Mapped[str] = mapped_column(String, nullable=False)
# # case study can have list of questions (one-to-many relationship with Question model)
# case_studu_questions: Mapped[List["Question"]] = relationship(
#     "Question", back_populates="case_study"
# )
