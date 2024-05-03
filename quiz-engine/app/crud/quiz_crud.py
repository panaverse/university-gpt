from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import and_, delete, select, Session

from app.core.config import logger_config
from app.models.question_models import QuestionBank
from app.models.quiz_models import (
    Quiz,
    QuizCreate,
    QuizQuestion,
    QuizUpdate,
)
from app.models.topic_models import Topic

logger = logger_config(__name__)

class CRUDQuizEngine:
    def _fetch_all_subtopics(self, *, topic_ids: list[int], db: Session):
        topics_and_subtopics = db.exec(
            select(Topic)
            .options(selectinload(Topic.children_topics))  # type:ignore
            .where(Topic.id.in_(topic_ids))  # type:ignore
        )  #
        topics_from_db = topics_and_subtopics.all()

        print("\n---------topics_from_db--------\n", topics_from_db)

        if not topics_from_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incorrect Topic IDs Provided",
            )

        all_topic_data = []
        all_topic_ids = set()

        def fetch_subtopics(topic_ids):
            nonlocal all_topic_data, all_topic_ids
            topics_result = db.exec(
                select(Topic)
                .options(selectinload(Topic.children_topics))
                .where(Topic.id.in_(topic_ids))
            )
            topics = topics_result.all()
            # for topic in topics:
            for topic in topics:
                if topic not in all_topic_data:
                    all_topic_data.append(topic)  # Store the topic object
                    all_topic_ids.add(topic.id)  # Store the topic ID
                if topic.children_topics:
                    child_topic_ids = [child.id for child in topic.children_topics]
                    fetch_subtopics(child_topic_ids)

        fetch_subtopics(topic_ids)

        return all_topic_ids, all_topic_data

    # Create Quiz
    def create_quiz(self, *, quiz: QuizCreate, db: Session):
        try:
            question_ids_with_topics: list = []  # Store tuples of (question_id, topic_id)
            topic_from_db = []

            # Get all topics if topic_ids are provided and append to quiz.topics
            if quiz.add_topic_ids:
                all_topic_ids, all_topic_data = self._fetch_all_subtopics(
                    topic_ids=quiz.add_topic_ids, db=db
                )

                print("\n----all_topic_ids----\n", all_topic_ids)

                # Fetch all unique questions linked to these topics and subtopics
                questions_result = db.exec(
                    select(QuestionBank.id, QuestionBank.topic_id).where(
                        QuestionBank.topic_id.in_(all_topic_ids),  # type:ignore
                        QuestionBank.is_verified == True,
                    )
                )  # type:ignore

                all_questions = questions_result.all()

                print(
                    "\n----questions_result----\n",
                    "\n\n\n",
                    all_questions,
                )

                question_ids_with_topics.extend(all_questions)

                print(
                    "\n\n\n----question_ids_with_topics----\n\n\n",
                    question_ids_with_topics,
                )

                # Append the topics to the quiz
                topic_from_db.extend(all_topic_data)

                print("\n----TOPICS_FROM_DB----\n", topic_from_db)

            quiz_to_db = Quiz.model_validate(quiz)
            quiz_to_db.topics = topic_from_db
            db.add(quiz_to_db)
            db.commit()
            db.refresh(quiz_to_db)

            if question_ids_with_topics:
                quiz_questions_instances = [
                    QuizQuestion(quiz_id=quiz_to_db.id, question_id=q_id, topic_id=t_id)
                    for q_id, t_id in question_ids_with_topics
                ]
                print("\n----quiz_questions_instances----\n", quiz_questions_instances)
                db.add_all(quiz_questions_instances)

            db.commit()
            # db.refresh(quiz_to_db)

            print("\n----quiz_to_db----\n", quiz_to_db)
            print("\n----quiz_to_db.id----\n", quiz_to_db.id)

            # Fetch the quiz with the topics and questions
            quiz_added = self.read_quiz_by_id(quiz_id=quiz_to_db.id, db=db)  # type:ignore

            print("\n----quiz_added.total_points----\n", quiz_added.total_points)

            # Update quiz points - based on the sum of all question points
            quiz_added.total_points = sum(
                [
                    quiz_question.question.points
                    for quiz_question in quiz_added.quiz_questions
                ]
            )
            print("\n----quiz_added.total_points----\n", quiz_added.total_points)

            db.commit()
            # db.refresh(quiz_added)

            return quiz_added

        except HTTPException as http_err:
            db.rollback()
            logger.error(f"create_quiz Error: {http_err}")
            raise http_err

        except Exception as e:
            db.rollback()
            logger.error(f"create_quiz Error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def read_all_quizzes_for_course(
        self, *, db: Session, course_id: int, offset: int, limit: int
    ):
        try:
            result = db.exec(
                select(Quiz)
                .options(selectinload(Quiz.topics))  # type:ignore
                .where(Quiz.course_id == course_id)
                .offset(offset)
                .limit(limit)
            )
            quizzes = result.all()
            if not quizzes:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Quizzes not found"
                )
            return quizzes
        except HTTPException as e:
            db.rollback()
            logger.error(f"read_all_quizzes Error: {e}")
            raise e
        except Exception as e:
            db.rollback()
            logger.error(f"read_all_quizzes Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in fetching Quizzes",
            )

    def read_quiz_by_id(self, *, quiz_id: int, db: Session):
        try:
            # quiz = db.get(Quiz, quiz_id)
            result = db.exec(
                select(Quiz)
                .options(
                    selectinload(Quiz.topics),  # type:ignore
                    selectinload(Quiz.quiz_settings),  # type:ignore
                    selectinload(
                        Quiz.quiz_questions  # type:ignore
                    ).joinedload(QuizQuestion.question),  # type:ignore
                )
                .where(Quiz.id == quiz_id)  # type:ignore
            )
            quiz = result.one()
            if not quiz:
                raise ValueError("Quiz not found")
            return quiz
        except ValueError as e:
            db.rollback()
            logger.error(f"read_quiz Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )
        except Exception as e:
            db.rollback()
            logger.error(f"read_quiz Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quiz"
            )

    def _add_new_topics(
        self, quiz_to_update, new_topic_ids, existing_topic_ids, db
    ):
        newly_added_topic_ids = set()
        if new_topic_ids:
            new_topics_with_subtopics = db.exec(
                select(Topic)
                .options(selectinload(Topic.children_topics))
                .where(Topic.id.in_(new_topic_ids))
            )
            for topic in new_topics_with_subtopics.all():
                if topic.id not in existing_topic_ids:
                    quiz_to_update.topics.append(topic)
                    newly_added_topic_ids.add(topic.id)
                for child in topic.children_topics:
                    if (
                        child.id not in existing_topic_ids
                        and child.id not in new_topic_ids
                    ):
                        quiz_to_update.topics.append(child)
                        newly_added_topic_ids.add(child.id)
            db.commit()
        return newly_added_topic_ids

    def _add_new_questions(self, quiz_id, newly_added_topic_ids, db):
        if newly_added_topic_ids:
            questions_result = db.execute(
                select(QuestionBank).where(
                    QuestionBank.topic_id.in_(list(newly_added_topic_ids)),
                    QuestionBank.is_verified == True,
                )
            )
            questions_to_add = questions_result.all()
            new_quiz_questions = [
                QuizQuestion(
                    quiz_id=quiz_id, question_id=question.id, topic_id=question.topic_id
                )
                for question in questions_to_add
            ]
            db.add_all(new_quiz_questions)
            db.commit()

    def _remove_topics(self, quiz_to_update, topics_to_remove, db):
        if topics_to_remove:
            # 1. Remove QuizTopic Link
            quiz_to_update.topics = [
                topic
                for topic in quiz_to_update.topics
                if topic.id not in topics_to_remove
            ]
            # 2. Remove QuizQuestion Link
            db.execute(
                delete(QuizQuestion).where(
                    QuizQuestion.question_id.in_(
                        select(QuestionBank.id).where(
                            QuestionBank.topic_id.in_(topics_to_remove)
                        )
                    ),
                    QuizQuestion.quiz_id == quiz_to_update.id,
                )
            )
            db.commit()

    def update_quiz(
        self, *, quiz_id: int, quiz_update_data: QuizUpdate, db: Session
    ):
        try:
            quiz_to_update = self.read_quiz_by_id(quiz_id=quiz_id, db=db)

            existing_topic_ids = {topic.id for topic in quiz_to_update.topics}
            new_topic_ids = (
                set(quiz_update_data.add_topic_ids) - existing_topic_ids
                if quiz_update_data.add_topic_ids
                else set()
            )
            topics_to_remove = (
                set(quiz_update_data.remove_topic_ids)
                if quiz_update_data.remove_topic_ids
                else set()
            )

            newly_added_topic_ids = self._add_new_topics(
                quiz_to_update, new_topic_ids, existing_topic_ids, db
            )
            self._add_new_questions(quiz_id, newly_added_topic_ids, db)
            self._remove_topics(quiz_to_update, topics_to_remove, db)

            for key, value in quiz_update_data.model_dump(exclude_unset=True).items():
                if hasattr(quiz_to_update, key):
                    setattr(quiz_to_update, key, value)

            db.commit()
            db.expire_all()

            quiz_updated = self.read_quiz_by_id(quiz_id=quiz_id, db=db)
            quiz_updated.total_points = sum(
                quiz_question_link.question.points
                for quiz_question_link in quiz_updated.quiz_questions
            )
            db.commit()

            return quiz_updated
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"update_quiz Error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def delete_quiz(self, *, quiz_id: int, db: Session):
        try:
            print("\n----quiz_id----\n", quiz_id)
            quiz_to_delete = db.get(Quiz, quiz_id)

            if not quiz_to_delete:
                raise ValueError("Quiz not found")

            print("\n----quiz_to_delete----\n", quiz_to_delete)

            logger.info(f"DELETE_QUIZ_TEST: {quiz_to_delete}")

            db.delete(quiz_to_delete)
            db.commit()

            return {"message": "Quiz deleted successfully!"}
        except ValueError as e:
            db.rollback()
            logger.error(f"delete_quiz Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )
        except Exception as e:
            db.rollback()
            logger.error(f"delete_quiz Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Error in deleting Quiz"
            )

# ------------------------------
# Quiz Generation Endpoint
# ------------------------------


class QuizRuntimeEngine:
    def generate_quiz(self, *, quiz_id: int, db: Session):
        try:
            # 1. Verify Student ID

            # 2. Verify Quiz ID and Quiz Key
            quiz_with_question_result = db.exec(
                select(Quiz)
                .options(
                    selectinload(Quiz.quiz_questions).joinedload(QuizQuestion.question)  # type:ignore  # type:ignore
                )
                .where(Quiz.id == quiz_id)
            )
            quiz_with_questions = quiz_with_question_result.one()

            if not quiz_with_questions:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
                )

            # 5. Return Quiz with Questions
            return quiz_with_questions

        except HTTPException as e:
            db.rollback()
            logger.error(f"generate_quiz Error: {e}")
            raise e
        except Exception as e:
            db.rollback()
            logger.error(f"generate_quiz Error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



# Initalize all the CRUD Classes
quiz_engine = CRUDQuizEngine()
runtime_quiz_engine = QuizRuntimeEngine()

