from fastapi import HTTPException, status
from sqlmodel import select, and_, Session

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.config import logger_config

from app.models.content_models import (
    Content,
    ContentCreate,
    ContentUpdate
)

logger = logger_config(__name__)

class ContentCRUD:
    def create_new_content(self, *, content: ContentCreate, db: Session):
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
            db.commit()
            db.refresh(content_to_db)
            return content_to_db
        except IntegrityError as e:
            db.rollback()
            # Logging the error might help in debugging, ensure logger is configured properly
            logger.error(f"CREATE_NEW_CONTENT: Integrity error occurred: {e}")
            # Raising HTTPException to inform the caller about the specific issue
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Foreign key constraint failed, the topic might not exist. {str(e)}",
            )
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"CREATE_NEW_CONTENT: Database operation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed. {str(e)}",
            )
        except Exception as e:
            db.rollback()
            logger.error(f"CREATE_NEW_CONTENT: Unexpected error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred. {str(e)}",
            )

    def read_content_for_topic(self, *, topic_id: int, db: Session):
        """
        Retrieve a list of content for a topic from the database.

        Args:
            topic_id (int): The ID of the topic to retrieve content for.
            db (optional) : Database Dependency Injection.

        Returns:
            List[Content]: A list of Content objects.

        """
        try:
            content = db.exec(select(Content).where(Content.topic_id == topic_id))
            contents = content.all()
            if not contents:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No content found"
                )
            return contents
        except HTTPException as e:
            db.rollback()
            logger.error(f"READ_TOPICS: No topics found: {e}")
            raise e  # Re-raise the HTTPException with the original status code and detail
        except IntegrityError as e:
            db.rollback()
            logger.error(f"READ_TOPICS: Integrity error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Foreign key constraint failed, the topic might not exist.",
            )
        except SQLAlchemyError as e:
            db.rollback()  # Ensure rollback is awaited
            logger.error(
                f"READ_TOPICS: A database error occurred while retrieving topics: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            )
        except Exception as e:
            db.rollback()  # Ensure rollback is awaited
            logger.error(f"READ_TOPICS: An unexpected error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            )

    def get_content_by_id(
        self, *, topic_id: int, content_id: int, db: Session
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
            result = db.exec(
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
            db.rollback()
            logger.error(f"GET_CONTENT_BY_ID: Content not found: {e}")
            raise e
        except IntegrityError as e:
            db.rollback()
            logger.error(f"GET_CONTENT_BY_ID: Integrity error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Foreign key constraint failed, the topic might not exist.",
            )
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"GET_CONTENT_BY_ID: Database operation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            )
        except Exception as e:
            db.rollback()
            logger.error(f"GET_CONTENT_BY_ID: Unexpected error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            )

    def update_content(
        self, *, id: int, content: ContentUpdate, db: Session
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
            content_to_update = db.get(Content, id)
            if not content_to_update:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
                )
            content_data = content.model_dump(exclude_unset=True)
            for key, value in content_data.items():
                setattr(content_to_update, key, value)
            db.add(content_to_update)
            db.commit()
            db.refresh(content_to_update)
            return content_to_update

        except HTTPException as e:
            db.rollback()
            logger.error(f"UPDATE_CONTENT: Content not found: {e}")
            raise e
        except IntegrityError as e:
            db.rollback()
            logger.error(f"UPDATE_CONTENT: Integrity error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Foreign key constraint failed, the topic might not exist.",
            )
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"UPDATE_CONTENT: Database operation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            )
        except Exception as e:
            db.rollback()
            logger.error(f"UPDATE_CONTENT: Unexpected error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            )

    def delete_content(self, *, id: int, db: Session):
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
            content = db.get(Content, id)
            if not content:
                raise ValueError("Content not found")
            db.delete(content)
            db.commit()
            return {"message": "Content deleted successfully"}
        except ValueError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting content",
            )



content_crud = ContentCRUD()
