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
from sqlalchemy.orm import Session, Query

# LOCAL LIBRARY IMPORTS
from src.database.database import SESSION_MAKER
from src.database.models.blog_post import BlogPost

from src.models.blog_post_model import BlogPostModel, BlogPostFilterModel


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

    def get_blog_posts(
        self: "BlogPostRepository", filters: BlogPostFilterModel
    ) -> list[BlogPost]:
        """
        Get all blog posts from the database.

        Returns:
        """

        query: Query = self.session.query(BlogPost)

        if filters.post_name is not None:
            query = query.filter(BlogPost.post_name == filters.post_name)

        if filters.description is not None:
            query = query.filter(BlogPost.description.ilike(f"%{filters.description}%"))

        if filters.text is not None:
            query = query.filter(BlogPost.text.ilike(f"%{filters.text}%"))

        if filters.released is not None:
            query = query.filter(BlogPost.released == filters.released)

        return query.all()

    def insert_blog_post(self: "BlogPostRepository", blog_post: BlogPostModel) -> None:
        """
        Insert a new blog post into the database.
        """

        if self.check_if_exists(blog_post.post_name):
            raise ValueError(
                f"Blog post with name {blog_post.post_name} already exists"
            )

        self.session.add(BlogPost(blog_post=blog_post))
        self.session.commit()

    def check_if_exists(self: "BlogPostRepository", blog_post_name: str) -> bool:
        """
        Check if a blog post with the given name exists in the database.
        """

        return (
            self.session.query(BlogPost)
            .filter(BlogPost.post_name == blog_post_name)
            .count()
            > 0
        )

    def check_if_released(self: "BlogPostRepository", blog_post_name: str) -> bool:
        """
        Check if a blog post with the given name has been released.
        """

        blog_post: BlogPost | None = (
            self.session.query(BlogPost)
            .filter(BlogPost.image_name == blog_post_name)
            .first()
        )

        if blog_post is None:
            raise ValueError(f"Blog post not found: {blog_post_name}")

        return blog_post.released

    def update_description(self, blog_post_name: str, description: str) -> bool:
        """
        Update the description of a blog post.
        """

        blog_post: BlogPost | None = (
            self.session.query(BlogPost)
            .filter(BlogPost.post_name == blog_post_name)
            .first()
        )

        if blog_post is None:
            raise ValueError(f"Blog post not found: {blog_post_name}")

        blog_post.description = description
        self.session.commit()

        return True

    def update_text(self: "BlogPostRepository", post_name: str, text: str) -> bool:
        """
        Update the text of a blog post.
        """

        blog_post: BlogPost | None = (
            self.session.query(BlogPost).filter(BlogPost.post_name == post_name).first()
        )

        if blog_post is None:
            raise ValueError(f"Blog post not found: {post_name}")

        blog_post.text = text
        self.session.commit()

        return True

    def update_release(
        self: "BlogPostRepository", post_name: str, release: bool
    ) -> bool:
        """
        Update the release status of a blog post.
        """

        blog_post: BlogPost | None = (
            self.session.query(BlogPost).filter(BlogPost.post_name == post_name).first()
        )

        if blog_post is None:
            raise ValueError(f"Blog post not found: {post_name}")

        blog_post.released = release
        self.session.commit()

        return True
