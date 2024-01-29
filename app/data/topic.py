from app.data.common import Base, QuestionDifficultyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, Boolean, Enum, UUID, Text
import uuid

from app.data.university import Course


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
    course_id: Mapped["Course"] = mapped_column(
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

    # contents: A one-to-many relationship with the Content class. Each topic can have multiple contents associated with it.
    contents: Mapped[list["Content"]] = relationship(
        "Content", back_populates="topic")
    # Add this line
    quiz_topics: Mapped[list["app.data.quiz.QuizTopic"]] = relationship(
        "app.data.quiz.QuizTopic", back_populates="topic")

    # TODOs: Review = linked Topic tp Questions
    # Other Tables that have a relationship with Topic
    # questions: A one-to-many relationship with the Question class. Each topic can have multiple questions associated with it.
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="topic")


class Content(Base):
    __tablename__ = 'contents'

    content_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_text: Mapped[str] = mapped_column(String)
    topic_id: Mapped[UUID] = mapped_column(ForeignKey('topics.topic_id'))
    # topic: A many-to-one relationship with the Topic class, indicating that each content is associated with a single topic.
    topic: Mapped["Topic"] = relationship("Topic", back_populates="contents")


class Question(Base):
    """
    Question model represents a question in the system. It contains fields like question_text, question_type, question_options, question_answer, question_explanation, and question_difficulty. It also has a many-to-one relationship with the Topic model, meaning a question is associated with a topic.
    """

    __tablename__ = "questions"
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    question_text: Mapped[str] = mapped_column(String, nullable=False)
    question_difficulty: Mapped[QuestionDifficultyEnum] = mapped_column(
        Enum(QuestionDifficultyEnum), nullable=False
    )
    question_points: Mapped[int] = mapped_column(String, nullable=False)
    topic_id: Mapped[UUID] = mapped_column(
        ForeignKey('topics.topic_id'), nullable=False)

    # relationships to the Topics table
    topic: Mapped["Topic"] = relationship("Topic", back_populates="questions")

    __mapper_args__ = {
        'polymorphic_identity': 'questions',
        'polymorphic_on': 'type'
    }

    type: Mapped[str] = mapped_column(String, nullable=False)


class SingleMCQQuestion(Question):
    __tablename__ = 'single_mcq_questions'

    single_mcq_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('questions.question_id'), primary_key=True)
    # Inherits options relationship from Question

    # Specific relationship for MCQs to Options
    options: Mapped[list["SingleSelectOptions"]] = relationship(
        "SingleSelectOptions", back_populates="single_select_mcq")

    case_study_id: Mapped[UUID] = mapped_column(
        ForeignKey('case_studies.case_study_id'), nullable=True)
    case_study: Mapped["CastStudyQuestion"] = relationship(
        "CaseStudy", back_populates="single_mcqs")

    # This is a one-to-many relationship
    selected_answer: Mapped[list["app.data.quiz.SingleSelectMCQAnswer"]] = relationship(
        "app.data.quiz.SingleSelectMCQAnswer", back_populates="single_mcq")

    __mapper_args__ = {
        'polymorphic_identity': 'single_mcq_question',
    }


class MultiMCQQuestion(Question):
    __tablename__ = 'multi_mcq_questions'

    multi_mcq_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('questions.question_id'), primary_key=True)
    # Inherits options relationship from Question

    # Specific relationship for MCQs to Options
    options: Mapped[list["MultiSelectOptions"]] = relationship(
        "MultiSelectOptions", back_populates="multi_select_mcq_option")

    case_study_id: Mapped[UUID] = mapped_column(
        ForeignKey('case_studies.case_study_id'), nullable=True)
    # case_study: Mapped["CastStudyQuestion"] = relationship("CaseStudy", back_populates="multi_mcqs")

    # This is a one-to-many relationship
    multi_select_mcq_answer: Mapped[list["app.data.quiz.MultiSelectMCQAnswer"]] = relationship(
        "app.data.quiz.MultiSelectMCQAnswer", back_populates="option_selected_relation")

    __mapper_args__ = {
        'polymorphic_identity': 'multi_mcq_question',
    }


class FreeTextQuestion(Question):
    __tablename__ = 'free_text_questions'

    free_text_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('questions.question_id'), primary_key=True)
    correct_answer: Mapped[str] = mapped_column(Text)

    #  This is a one-to-many relationship
    answers: Mapped[list["app.data.quiz.FreeTextAnswer"]] = relationship(
        "app.data.quiz.FreeTextAnswer", back_populates="question")

    __mapper_args__ = {
        'polymorphic_identity': 'free_text_questions',
    }


class CodingQuestion(Question):
    __tablename__ = 'coding_questions'

    coding_question_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('questions.question_id'), primary_key=True)
    correct_answer: Mapped[str] = mapped_column(Text)

    # TODO: Afte Answers
    # This is a one-to-many relationship
    answers: Mapped[list["app.data.quiz.CodingAnswer"]] = relationship(
        "app.data.quiz.CodingAnswer", back_populates="question")

    __mapper_args__ = {
        'polymorphic_identity': 'coding_question',
    }


class CastStudyQuestion(Question):
    __tablename__ = 'case_studies'

    case_study_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('questions.question_id'), primary_key=True)

    single_mcqs: Mapped[list["SingleMCQQuestion"]] = relationship(
        "SingleMCQQuestion", back_populates="case_study")

    # multi_mcqs: Mapped[list["MultiMCQQuestion"]] = relationship("MultiMCQQuestion", back_populates="case_study")

    # TODO: Afte Answers
    # This is a one-to-many relationship
    # answers: Mapped[list["app.models.quiz.CodingAnswer"]] = relationship("app.models.quiz.CodingAnswer", back_populates="question")

    __mapper_args__ = {
        'polymorphic_identity': 'case_study_question',
    }


class SingleSelectOptions(Base):
    """
    Option model represents an option for a question in the system. It contains fields like option_text and option_is_correct. It also has a many-to-one relationship with the Question model, meaning an option is associated with a question.
    """

    __tablename__ = "single_select_options"
    single_select_option_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    option_text: Mapped[str] = mapped_column(String, nullable=False)
    option_is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # TODO: Update relationship & Foreign Key
    single_select_mcq: Mapped["SingleMCQQuestion"] = mapped_column(
        ForeignKey("single_mcq_questions.single_mcq_id"), nullable=True
    )
    option_question: Mapped["SingleMCQQuestion"] = relationship(
        "SingleMCQQuestion", back_populates="options"
    )


class MultiSelectOptions(Base):
    """
    Option model represents an option for a question in the system. It contains fields like option_text and option_is_correct. It also has a many-to-one relationship with the Question model, meaning an option is associated with a question.
    """

    __tablename__ = "multi_select_options"
    multi_select_option_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    option_text: Mapped[str] = mapped_column(String, nullable=False)
    option_is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # TODO: Update relationship & Foreign Key
    option_question_id: Mapped["MultiMCQQuestion"] = mapped_column(
        ForeignKey("multi_mcq_questions.multi_mcq_id"), nullable=True
    )
    multi_select_mcq_option: Mapped["MultiMCQQuestion"] = relationship(
        "MultiMCQQuestion", back_populates="options"
    )
