from fastapi import HTTPException, status
from sqlmodel import select, Session

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import selectinload

from app.core.config import logger_config

from app.models.topic_models import (
    Topic,
    TopicCreate,
    TopicUpdate,
)
from app.models.content_models import Content

logger = logger_config(__name__)


class TopicCRUD:
    def create_topic(self, *, topic: TopicCreate, db: Session):
        """
        Create a new topic or subtopic in the database.

        Args:
            topic (TopicCreate): The topic data to be created.
            db (Session): The database session.

        Returns:
            Topic: The created topic.

        Raises:
            ValueError: For data integrity issues.
            SQLAlchemyError: For database operation errors.
            Exception: For unexpected errors.
        """
        try:
            # Validate and add associated contents if present
            if topic.contents:
                topic.contents = [
                    Content.model_validate(content)
                    for content in topic.contents  # type:ignore
                ]
            # Transform TopicCreate schema into Topic model instance
            topic_to_db = Topic.model_validate(topic)

            # Add the new topic to the database and commit the transaction
            db.add(topic_to_db)
            db.commit()
            db.refresh(topic_to_db)

            return topic_to_db

        except IntegrityError as e:
            db.rollback()  # Ensure rollback is awaited
            logger.error(
                f"CREATE_TOPIC: An integrity error occurred while creating the topic: {e}"
            )
            raise ValueError("Data integrity issue.") from e

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(
                f"CREATE_TOPIC: A database error occurred while creating the topic: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed. {str(e)}",
            )

        except Exception as e:
            db.rollback()
            logger.error(f"CREATE_TOPIC: An unexpected error occurred: {e}")
            raise Exception("An unexpected error occurred.") from e

    def read_topics(self, *, offset: int, per_page: int, db: Session):
        """
        Retrieve a list of topics from the database.
        Args:
            offset (int): The number of topics to skip before starting to return results.
            per_page (int): The maximum number of topics to return per_page.
            db (optional) : Database Dependency Injection.

        Returns:
            List[Topic]: A list of Topic objects.

        Raises:
            HTTPException: If no topics are found or for other HTTP-related errors.
            SQLAlchemyError: For database operation errors.
            Exception: For unexpected errors.

        """
        
        try:
            if offset < 0:
                raise HTTPException(status_code=400, detail="Offset cannot be negative")
            if per_page < 1:
                raise HTTPException(status_code=400, detail="Per page items cannot be less than 1")
            
            topics = db.exec(select(Topic).offset(offset).limit(per_page)).all()
            if topics is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No topics found"
                )
            return topics
        except HTTPException as e:
            db.rollback()
            logger.error(f"READ_TOPICS: No topics found: {e}")
            raise e  # Re-raise the HTTPException with the original status code and detail
        except SQLAlchemyError as e:
            db.rollback()  # Ensure rollback is awaited
            logger.error(
                f"READ_TOPICS: A database error occurred while retrieving topics: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed. {str(e)}",
            )
        except Exception as e:
            db.rollback()  # Ensure rollback is awaited
            logger.error(f"READ_TOPICS: An unexpected error occurred: {e}")
            raise Exception("An unexpected error occurred.") from e

    def read_topic_by_id(self, *, id: int, db: Session):
        """
        Retrieve a topic by its ID.

        Args:
            id (int): The ID of the topic to retrieve.
            db (optional) : Database Dependency Injection.

        Returns:
            Topic: The retrieved topic.

        Raises:
            HTTPException
        """
        try:
            # topic = db.get(Topic, id)
            result = db.exec(
                select(Topic)
                .options(selectinload(Topic.contents))  # type:ignore
                .where(Topic.id == id)
            )
            topic = result.one_or_none()
            if not topic:
                raise ValueError("Topic not found")
            return topic

        except ValueError as e:
            db.rollback()  # Ensure rollback is awaited
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
            ) 

        except SQLAlchemyError as e:
            db.rollback()  # Ensure rollback is awaited
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            ) from e
        except HTTPException as http_err:
            db.rollback()
            raise http_err
        except Exception as e:
            db.rollback()  # Ensure rollback is awaited
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            ) from e

    def read_topic_and_subtopics(self, *, id: int, db: Session):
        try:
            topic_result = db.exec(
                select(Topic)
                .options(
                    selectinload(Topic.children_topics),  # type:ignore
                    selectinload(Topic.parent_topic),  # type:ignore
                )
                .where(Topic.id == id)
            )
            topic = topic_result.one_or_none()

            if topic is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
                )

            parent_topic_id = topic.parent_topic.id if topic.parent_topic else None
            # children_topic_ids = [child.id for child in topic.children_topics]

            # Recursively get the children topics
            children_topics = []
            for child in topic.children_topics:
                if child.id is not None:
                    child_topic = self.read_topic_and_subtopics(
                        id=child.id, db=db
                    )
                    children_topics.append(child_topic)

            return {
                "topic_id": topic.id,
                "title": topic.title,
                "description": topic.description,
                "parent_topic_id": parent_topic_id,
                # "children_topic_ids": children_topic_ids,
                "children_topics": children_topics,
            }

        except ValueError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        except HTTPException as http_err:
            db.rollback()
            raise http_err
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def update_topic(self, *, id: int, topic: TopicUpdate, db: Session):
        """
        Update a topic in the database.

        Args:
            id (int): The ID of the topic to update.
            topic (TopicUpdate): The updated topic data.
            db (optional) : Database Dependency Injection.

        Returns:
            Topic: The updated topic.

        Raises:
            ValueError: If the topic with the given ID is not found.
        """
        try:
            topic_to_update = db.get(Topic, id)
            if not topic_to_update:
                raise ValueError("Topic not found")
            topic_data = topic.model_dump(exclude_unset=True)
            topic_to_update.sqlmodel_update(topic_data)
            db.add(topic_to_update)
            db.commit()
            db.refresh(topic_to_update)
            return topic_to_update
        except ValueError:
            db.rollback()
            logger.error("UPDATE_TOPIC: Topic not found")
            raise ValueError("Topic not found")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"UPDATE_TOPIC: Error updating topic: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating topic {str(e)}",
            )
        except Exception as e:
            db.rollback()
            logger.error(f"UPDATE_TOPIC: Error updating topic: {str(e)}")
            raise Exception("Error updating topic")

    def delete_topic(self, *, id: int, db: Session):
        """
        Deletes a topic from the database based on the provided ID.

        Args:
            id (int): The ID of the topic to be deleted.
            db (optional) : Database Dependency Injection.

        Raises:
            HTTPException: If the topic with the provided ID is not found.

        Returns:
            dict: A dictionary with a message indicating the successful deletion of the topic.
        """
        try:
            topic = db.get(Topic, id)
            if not topic:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
                )
            db.delete(topic)
            db.commit()
            return {"message": "Topic deleted successfully"}
        except HTTPException:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting topic",
            )


    def count_records(self, *, db: Session) -> int:
        try:
            query = select(Topic.title)
            items = db.exec(query).all()
            count = len(items)
            return count
        except Exception as e:
            db.rollback()
            # Log the exception for debugging purposes
            print(f"Error counting SearchToolRecord items: {e}")
            # Re-raise the exception to be handled at the endpoint level
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        
topic_crud = TopicCRUD()
