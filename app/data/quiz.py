from app.data.common import Base, QuizStatusEnum
from typing import List
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, Integer, Enum, UUID, DateTime, Float, Text
import uuid

from app.data.topic import Topic, FreeTextQuestion, CodingQuestion, SingleMCQQuestion
from app.data.university import Course
from app.data.user import Student


class Quiz(Base):
    """
    Quiz model represents a quiz in the system. It contains fields like quiz_name and quiz_description. It also has a many-to-one relationship with the Topic model, meaning a quiz is associated with a topic. Additionally, it has a one-to-many relationship with the Question model, meaning a quiz can have many questions associated with it.
    """

    __tablename__ = "quizzes"
    quiz_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    quiz_name: Mapped[str] = mapped_column(String, nullable=False)
    quiz_time_limit_mins: Mapped[int] = mapped_column(Integer, nullable=False)

    quiz_description: Mapped[str] = mapped_column(String, nullable=True)

    # A many-to-one relationship with the Course class, meaning a single course can have multiple quizzes.
    course_id: Mapped[UUID] = mapped_column(ForeignKey('courses.course_id'))
    course: Mapped["Course"] = relationship("Course", back_populates="quizzes")

    # A one-to-many relationship with the QuizTopic class.
    # back_populates attribute is used to ensure that the relationship is bidirectional.
    quiz_topics: Mapped[list["QuizTopic"]] = relationship(
        "QuizTopic", back_populates="quiz")

    # A one-to-many relationship with the QuizAnswerSheet class, meaning a single quiz can have multiple answer sheets.
    answer_sheets: Mapped[list["QuizAnswerSheet"]] = relationship(
        "QuizAnswerSheet", back_populates="quiz")


class QuizTopic(Base):
    __tablename__ = 'quiz_topic'
    quiz_topic_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id: Mapped[UUID] = mapped_column(ForeignKey('quizzes.quiz_id'))
    topic_id: Mapped[UUID] = mapped_column(ForeignKey('topics.topic_id'))

    # https://docs.sqlalchemy.org/en/20/orm/self_referential.html
    # establishing subtopic_id as the “local” side, and the relationship then behaves as a many-to-one.
    parent_quiz_topic_id: Mapped[UUID] = mapped_column(
        ForeignKey('quiz_topic.quiz_topic_id'), nullable=True)
    # self referential relationship
    children_quiz_topic = relationship(
        "QuizTopic", back_populates="parent_quiz_topic")
    parent_quiz_topic = relationship(
        "QuizTopic", back_populates="children_quiz_topic", remote_side=[quiz_topic_id])

    # Relationships
    #  A many-to-one relationship with the Quiz class, meaning multiple quiz topics can relate back to a single quiz.
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="quiz_topics")
    topic: Mapped["Topic"] = relationship(
        "Topic", back_populates="quiz_topics")


class QuizAnswerSheet(Base):
    __tablename__ = 'quiz_answer_sheets'

    answer_sheet_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # student_id: A foreign key linking to the students table, indicating which student the quiz is associated with.
    student_id: Mapped[UUID] = mapped_column(
        ForeignKey('students.student_id'), nullable=False)
    quiz_id: Mapped[UUID] = mapped_column(
        ForeignKey('quizzes.quiz_id'), nullable=False)

    quiz_status: Mapped[QuizStatusEnum] = mapped_column(
        Enum(QuizStatusEnum), default=QuizStatusEnum.TO_DO)
    start_date: Mapped[DateTime] = mapped_column(DateTime)
    end_date: Mapped[DateTime] = mapped_column(DateTime)

    # A many-to-one relationship with the Student class, meaning multiple quizzes can be associated with a single student.
    # back_populates attribute is used to ensure that the relationship is bidirectional.
    student: Mapped["Student"] = relationship(
        "Student", back_populates="quiz_answer_sheets")

    # Relationships
    # A one-to-many relationship with the Answer class, meaning a single answer sheet can have multiple answers.
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="answer_sheets")
    answers: Mapped[list["Answer"]] = relationship(
        "Answer", back_populates="answer_sheet")


# Define the Answer hierarchy here
class Answer(Base):
    __tablename__ = 'answers'

    answer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    answer_sheet_id: Mapped[UUID] = mapped_column(ForeignKey(
        'quiz_answer_sheets.answer_sheet_id'), nullable=False)
    points_received: Mapped[float] = mapped_column(Float, nullable=True)
    # A many-to-one relationship with the QuizAnswerSheet class, meaning a single answer is associated with one answer sheet.
    answer_sheet: Mapped["QuizAnswerSheet"] = relationship(
        "QuizAnswerSheet", back_populates="answers")

    __mapper_args__ = {
        'polymorphic_identity': 'answers',
        'polymorphic_on': 'type'
    }

    type: Mapped[str] = mapped_column(String, nullable=False)


class FreeTextAnswer(Answer):
    __tablename__ = 'free_text_answers'

    # composite primary key
    answer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('answers.answer_id'), primary_key=True)
    filled_answer: Mapped[str] = mapped_column(Text)

    free_text_question_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('free_text_questions.free_text_id'))

    # This is a many-to-one relationship
    question: Mapped["FreeTextQuestion"] = relationship(
        "FreeTextQuestion", back_populates="answers")

    __mapper_args__ = {
        'polymorphic_identity': 'free_text_answer',
    }


class CodingAnswer(Answer):
    __tablename__ = 'coding_answers'

    # composite primary key
    answer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('answers.answer_id'), primary_key=True)
    filled_answer: Mapped[str] = mapped_column(Text)

    coding_question_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('coding_questions.coding_question_id'))
    # This is a many-to-one relationship
    question: Mapped["CodingQuestion"] = relationship(
        "CodingQuestion", back_populates="answers")

    __mapper_args__ = {
        'polymorphic_identity': 'coding_answer',
    }


class CaseStudyAnswer(Answer):
    __tablename__ = 'case_studies_answers'

    # composite primary key
    answer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('answers.answer_id'), primary_key=True)

    join_case_study_answer: Mapped[list["JoinCaseStudyAnswer"]] = relationship(
        "JoinCaseStudyAnswer", back_populates="case_study_answer")

    __mapper_args__ = {
        'polymorphic_identity': 'case_study_answer',
    }

# Join Table to Get all Answers/SINGLESELECTMCW & Answer


class JoinCaseStudyAnswer(Base):
    __tablename__ = 'join_case_study_answers'

    join_case_study_answers_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    case_study_answer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('case_studies_answers.answer_id'))
    case_study_answer: Mapped["CaseStudyAnswer"] = relationship(
        "CaseStudyAnswer", back_populates="join_case_study_answer")

    single_select_mcq_answer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True))


class SingleSelectMCQAnswer(Answer):
    __tablename__ = 'single_mcq_select_answer'

    # composite primary key
    answer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('answers.answer_id'), primary_key=True)
    selected_mcq_id: Mapped[UUID] = mapped_column(UUID)

    single_select_mcq_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('single_mcq_questions.single_mcq_id'))
    # This is a many-to-one relationship
    single_mcq: Mapped["SingleMCQQuestion"] = relationship(
        "SingleMCQQuestion", back_populates="selected_answer")

    __mapper_args__ = {
        'polymorphic_identity': 'single_mcq_select_answer',
    }


class MultiSelectMCQAnswer(Answer):
    __tablename__ = 'multi_mcq_select_answer'

    # composite primary key
    answer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('answers.answer_id'), primary_key=True)
    selected_mcq_id: Mapped[UUID] = mapped_column(UUID)

    option_selected_relation = relationship(
        "OptionMultiSelectAnswers", back_populates="multi_select_mcq_answer")

    __mapper_args__ = {
        'polymorphic_identity': 'multi_mcq_select_answer',
    }


class OptionMultiSelectAnswers(Base):
    __tablename__ = 'option_multi_select_answers'

    option_multi_select_answers_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foriegn Key to MultiSelectMCQAnswer
    multi_select_mcq_answer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('multi_mcq_select_answer.answer_id'))

    select_mcq_id: Mapped[UUID] = mapped_column(UUID)

    multi_select_mcq_answer: Mapped[list["MultiSelectMCQAnswer"]] = relationship(
        "MultiSelectMCQAnswer", back_populates="option_selected_relation")
