"""
file_name = blog_post.py
Created On: 2024/07/09
Lasted Updated: 2024/07/09
Description: _FILL OUT HERE_
Edit Log:
2024/07/09
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import mapped_column, Mapped

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS
from database.database import BASE
from src.models.blog_post_model import BlogPostModel


class BlogPost(BASE):
    """
    A model for the blog post table
    """

    __tablename__ = "blog_posts"

    post_name: Mapped[str] = mapped_column(
        String(256), primary_key=True, unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    released: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    release_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_updated: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    def __init__(self, blog_post: BlogPostModel):
        self.post_name = blog_post.post_name
        self.description = blog_post.description
        self.text = blog_post.text
        self.released = blog_post.released
