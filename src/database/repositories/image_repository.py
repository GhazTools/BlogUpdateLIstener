"""
file_name = image_repository.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from sqlalchemy.orm import Session, Query

# LOCAL LIBRARY IMPORTS
from src.database.database import SESSION_MAKER
from src.database.models.image import Image

from src.models.image_model import ImageModel, ImageFilterModel


class ImageRepository:
    """
    A class to handle the image repository
    """

    def __init__(self: "ImageRepository") -> None:
        """
        Create a new ImageRepository and initialize the session
        """

        self.session: Session = SESSION_MAKER()

    def __enter__(self: "ImageRepository") -> "ImageRepository":
        """
        Called when the object is used as a context manager.

        This function is called when the `with` statement is used to create a context
        for the EndpointDiagnosticsRepository object. Returns the current object as the context
        manager value.
        """

        return self  # pylint: disable=unnecessary-pass

    def __exit__(self: "ImageRepository", type, value, traceback) -> None:  # pylint: disable=redefined-builtin
        """
        Called when the context manager is exited.

        This function is called when the `with` block created by the `with` statement
        that created this context manager is exited. This function closes the SQLAlchemy
        session.
        """

        self.session.close()

    def get_images(self: "ImageRepository", filters: ImageFilterModel) -> list[Image]:
        """
        Get all images from the database.

        Returns:
            A list of all images in the database.
        """

        query: Query = self.session.query(Image)

        # TODO: Create an extendable filter model

        if filters.image_name is not None:
            query = query.filter(Image.image_name == filters.image_name)

        if filters.released is not None:
            query = query.filter(Image.released == filters.released)

        return query.all()

    def insert_image(self: "ImageRepository", image: ImageModel) -> None:
        """
        Insert a new image into the database.

        Args:
            image: The image to insert.
        """

        if self.check_if_exists(image.image_name):
            raise ValueError("Image already exists")

        self.session.add(Image(image))
        self.session.commit()

    def check_if_exists(self: "ImageRepository", image_name: str) -> bool:
        """
        Check if an image with the given name exists in the database.

        Args:
            image_name: The name of the image to check for.

        Returns:
            True if the image exists, False otherwise.
        """

        return (
            self.session.query(Image).filter(Image.image_name == image_name).count() > 0
        )

    def check_if_released(self: "ImageRepository", image_name: str) -> bool:
        """
        Check if an image with the given name has been released.

        Args:
            image_name: The name of the image to check for.

        Returns:
            True if the image has been released, False otherwise.
        """

        image: Image | None = (
            self.session.query(Image).filter(Image.image_name == image_name).first()
        )

        if image is None:
            raise ValueError(f"Image not found: {image_name}")

        return image.released

    def update_release(self: "ImageRepository", image_name: str, release: bool) -> bool:
        """
        Update the release state of an image

        Args:
            image_name: The name of the image to update release for.

        Returns:
            True if the image release attribute was updated, False otherwise.
        """

        image: Image | None = (
            self.session.query(Image).filter(Image.image_name == image_name).first()
        )

        if image is None:
            raise ValueError(f"Image not found: {image_name}")

        image.released = release
        self.session.commit()

        return True

    def delete_image(self: "ImageRepository", image_name: str) -> bool:
        """
        Delete an image from the database.

        Args:
            image_name: The name of the image to delete.

        Returns:
            True if the image was deleted, False otherwise.
        """

        image: Image | None = (
            self.session.query(Image).filter(Image.image_name == image_name).first()
        )

        if image is None:
            raise ValueError(f"Image not found: {image_name}")

        self.session.delete(image)
        self.session.commit()

        return True
