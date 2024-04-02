from fastapi import HTTPException, status
from sqlmodel import select, and_

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import selectinload


from app.core.db import AsyncSession
from app.core.config import logger_config

from app.models.topic_models import (
    Topic,
    TopicCreate,
    TopicUpdate,
    Content,
    ContentCreate,
    ContentUpdate,
)

logger = logger_config(__name__)


class TopicCRUD:
    async def create_topic(self, *, topic: TopicCreate, db: AsyncSession):
        """
        Create a new topic or subtopic in the database.

        Args:
            topic (TopicCreate): The topic data to be created.
            db (AsyncSession): The database session.

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
            await db.commit()
            await db.refresh(topic_to_db)

            return topic_to_db

        except IntegrityError as e:
            await db.rollback()  # Ensure rollback is awaited
            logger.error(
                f"CREATE_TOPIC: An integrity error occurred while creating the topic: {e}"
            )
            raise ValueError("Data integrity issue.") from e

        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(
                f"CREATE_TOPIC: A database error occurred while creating the topic: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed. {str(e)}",
            )

        except Exception as e:
            await db.rollback()
            logger.error(f"CREATE_TOPIC: An unexpected error occurred: {e}")
            raise Exception("An unexpected error occurred.") from e

    async def read_topics(self, *, offset: int, limit: int, db: AsyncSession):
        """
        Retrieve a list of topics from the database.
        Args:
            offset (int): The number of topics to skip before starting to return results.
            limit (int): The maximum number of topics to return.
            db (optional) : Database Dependency Injection.

        Returns:
            List[Topic]: A list of Topic objects.

        Raises:
            HTTPException: If no topics are found or for other HTTP-related errors.
            SQLAlchemyError: For database operation errors.
            Exception: For unexpected errors.

        """
        try:
            result = await db.exec(select(Topic).offset(offset).limit(limit))
            topics = result.all()
            if not topics:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No topics found"
                )
            return topics
        except HTTPException as e:
            await db.rollback()
            logger.error(f"READ_TOPICS: No topics found: {e}")
            raise e  # Re-raise the HTTPException with the original status code and detail
        except SQLAlchemyError as e:
            await db.rollback()  # Ensure rollback is awaited
            logger.error(
                f"READ_TOPICS: A database error occurred while retrieving topics: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed. {str(e)}",
            )
        except Exception as e:
            await db.rollback()  # Ensure rollback is awaited
            logger.error(f"READ_TOPICS: An unexpected error occurred: {e}")
            raise Exception("An unexpected error occurred.") from e

    async def read_topic_by_id(self, *, id: int, db: AsyncSession):
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
            # topic = await db.get(Topic, id)
            result = await db.exec(
                select(Topic)
                .options(selectinload(Topic.contents))  # type:ignore
                .where(Topic.id == id)
            )
            topic = result.one()
            if not topic:
                raise ValueError("Topic not found")
            return topic

        except ValueError as e:
            await db.rollback()  # Ensure rollback is awaited
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
            ) from e

        except SQLAlchemyError as e:
            await db.rollback()  # Ensure rollback is awaited
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            ) from e

        except Exception as e:
            await db.rollback()  # Ensure rollback is awaited
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            ) from e

    async def read_topic_and_subtopics(self, *, id: int, db: AsyncSession):
        try:
            topic_result = await db.exec(
                select(Topic)
                .options(
                    selectinload(Topic.children_topics),  # type:ignore
                    selectinload(Topic.parent_topic),  # type:ignore
                )
                .where(Topic.id == id)
            )
            topic = topic_result.one_or_none()

            if not topic:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
                )

            parent_topic_id = topic.parent_topic.id if topic.parent_topic else None
            # children_topic_ids = [child.id for child in topic.children_topics]

            # Recursively get the children topics
            children_topics = []
            for child in topic.children_topics:
                if child.id is not None:
                    child_topic = await self.read_topic_and_subtopics(
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

        # async def read_topic_and_subtopics(self, *, id: int, db: AsyncSession):
        #     try:
        #         TopicAlias = aliased(Topic)

        #         stmt = (
        #             select(Topic)
        #             .options(
        #                 selectinload(Topic.children_topics),  # type:ignore
        #                 selectinload(Topic.parent_topic),  # type:ignore
        #             )
        #             .where(Topic.id == id)
        #         )

        #         stmt = select([stmt]).cte("topics_cte", recursive=True)

        #         alias = stmt.alias()
        #         recursive = alias.union_all(
        #             select([TopicAlias]).where(TopicAlias.parent_id == alias.c.id)
        #         )

        #         stmt = select([alias]).union_all(recursive)

        #         result = await db.exec(stmt)

        #         topics = result.all()

        #         if not topics:
        #             raise HTTPException(
        #                 status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
        #             )

        #         return topics
        # Now topics contains all topics and subtopics. You can transform it into the desired format.

        except ValueError as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def update_topic(self, *, id: int, topic: TopicUpdate, db: AsyncSession):
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
            topic_to_update = await db.get(Topic, id)
            if not topic_to_update:
                raise ValueError("Topic not found")
            topic_data = topic.model_dump(exclude_unset=True)
            topic_to_update.sqlmodel_update(topic_data)
            db.add(topic_to_update)
            await db.commit()
            await db.refresh(topic_to_update)
            return topic_to_update
        except ValueError:
            await db.rollback()
            logger.error("UPDATE_TOPIC: Topic not found")
            raise ValueError("Topic not found")
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"UPDATE_TOPIC: Error updating topic: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating topic {str(e)}",
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"UPDATE_TOPIC: Error updating topic: {str(e)}")
            raise Exception("Error updating topic")

    async def delete_topic(self, *, id: int, db: AsyncSession):
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
            topic = await db.get(Topic, id)
            if not topic:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
                )
            await db.delete(topic)
            await db.commit()
            return {"message": "Topic deleted successfully"}
        except HTTPException:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
            )
        except Exception as e:
            await db.rollback()
            print(f"Error deleting topic: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting topic",
            )


class ContentCRUD:
    async def create_new_content(self, *, content: ContentCreate, db: AsyncSession):
        """
        Create a new content for a topic in the database.

        Args:
            content (ContentCreate): The content data to be created.
            db (optional) : Database Dependency Injection.

        Returns:
            Content: The created content.

        Raises:
            HTTPException: For specific handled errors such as IntegrityError.
            Exception: For unexpected errors.
        """
        try:
            content_to_db = Content.model_validate(content)
            db.add(content_to_db)
            await db.commit()
            await db.refresh(content_to_db)
            return content_to_db
        except IntegrityError as e:
            await db.rollback()
            # Logging the error might help in debugging, ensure logger is configured properly
            logger.error(f"CREATE_NEW_CONTENT: Integrity error occurred: {e}")
            # Raising HTTPException to inform the caller about the specific issue
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Foreign key constraint failed, the topic might not exist. {str(e)}",
            )
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"CREATE_NEW_CONTENT: Database operation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed. {str(e)}",
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"CREATE_NEW_CONTENT: Unexpected error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred. {str(e)}",
            )

    async def read_content_for_topic(self, *, topic_id: int, db: AsyncSession):
        """
        Retrieve a list of content for a topic from the database.

        Args:
            topic_id (int): The ID of the topic to retrieve content for.
            db (optional) : Database Dependency Injection.

        Returns:
            List[Content]: A list of Content objects.

        """
        try:
            content = await db.exec(select(Content).where(Content.topic_id == topic_id))
            contents = content.all()
            if not contents:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No content found"
                )
            return contents
        except HTTPException as e:
            await db.rollback()
            logger.error(f"READ_TOPICS: No topics found: {e}")
            raise e  # Re-raise the HTTPException with the original status code and detail
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"READ_TOPICS: Integrity error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Foreign key constraint failed, the topic might not exist.",
            )
        except SQLAlchemyError as e:
            await db.rollback()  # Ensure rollback is awaited
            logger.error(
                f"READ_TOPICS: A database error occurred while retrieving topics: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            )
        except Exception as e:
            await db.rollback()  # Ensure rollback is awaited
            logger.error(f"READ_TOPICS: An unexpected error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            )

    async def get_content_by_id(
        self, *, topic_id: int, content_id: int, db: AsyncSession
    ):
        """
        Retrieve a content by its ID.

        Args:
            topic_id (int): The ID of the topic for which content to retrieve.
            content_id (int): The ID of the content to retrieve.
            db (optional) : Database Dependency Injection.

        Returns:
            Content: The retrieved content.

        Raises:
            HTTPException: If the content with the given ID is not found.
        """

        try:
            result = await db.exec(
                select(Content).where(
                    and_(Content.topic_id == topic_id, Content.id == content_id)
                )
            )
            content = result.one_or_none()
            if not content:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
                )
            return content

        except HTTPException as e:
            await db.rollback()
            logger.error(f"GET_CONTENT_BY_ID: Content not found: {e}")
            raise e
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"GET_CONTENT_BY_ID: Integrity error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Foreign key constraint failed, the topic might not exist.",
            )
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"GET_CONTENT_BY_ID: Database operation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"GET_CONTENT_BY_ID: Unexpected error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            )

    async def update_content(
        self, *, id: int, content: ContentUpdate, db: AsyncSession
    ):
        """
        Update a content in the database.

        Args:
            id (int): The ID of the content to update.
            content (ContentUpdate): The updated content data.
            db (optional) : Database Dependency Injection.

        Returns:
            Content: The updated content.

        Raises:
            HTTPException: If the content with the given ID is not found.
        """
        try:
            content_to_update = await db.get(Content, id)
            if not content_to_update:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
                )
            content_data = content.model_dump(exclude_unset=True)
            for key, value in content_data.items():
                setattr(content_to_update, key, value)
            db.add(content_to_update)
            await db.commit()
            await db.refresh(content_to_update)
            return content_to_update

        except HTTPException as e:
            await db.rollback()
            logger.error(f"UPDATE_CONTENT: Content not found: {e}")
            raise e
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"UPDATE_CONTENT: Integrity error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Foreign key constraint failed, the topic might not exist.",
            )
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"UPDATE_CONTENT: Database operation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"UPDATE_CONTENT: Unexpected error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            )

    async def delete_content(self, *, id: int, db: AsyncSession):
        """
        Deletes a content from the database based on the provided ID.

        Args:
            id (int): The ID of the content to be deleted.
            db (optional) : Database Dependency Injection.

        Raises:
            HTTPException: If the content with the provided ID is not found.

        Returns:
            dict: A dictionary with a message indicating the successful deletion of the content.
        """
        try:
            content = await db.get(Content, id)
            if not content:
                raise ValueError("Content not found")
            await db.delete(content)
            await db.commit()
            return {"message": "Content deleted successfully"}
        except ValueError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
            )
        except Exception as e:
            await db.rollback()
            print(f"Error deleting content: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting content",
            )


topic_crud = TopicCRUD()
content_crud = ContentCRUD()
