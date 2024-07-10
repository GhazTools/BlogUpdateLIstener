"""
file_name = blog_post_repository.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from sqlalchemy.orm import Session

# LOCAL LIBRARY IMPORTS
from database.database import SESSION_MAKER


class BlogPostRepository:
    """
    A class to handle the image repository
    """

    def __init__(self: "BlogPostRepository") -> None:
        """
        Create a new ImageRepository and initialize the session
        """

        self.session: Session = SESSION_MAKER()

    def __enter__(self: "BlogPostRepository") -> "BlogPostRepository":
        """
        Called when the object is used as a context manager.

        This function is called when the `with` statement is used to create a context
        for the EndpointDiagnosticsRepository object. Returns the current object as the context
        manager value.
        """

        return self  # pylint: disable=unnecessary-pass

    def __exit__(self: "BlogPostRepository", type, value, traceback) -> None:  # pylint: disable=redefined-builtin
        """
        Called when the context manager is exited.

        This function is called when the `with` block created by the `with` statement
        that created this context manager is exited. This function closes the SQLAlchemy
        session.
        """

        self.session.close()
