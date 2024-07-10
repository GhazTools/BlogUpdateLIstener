"""
file_name = blog_post_model.py
Created On: 2024/07/09
Lasted Updated: 2024/07/09
Description: _FILL OUT HERE_
Edit Log:
2024/07/09
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from pydantic import BaseModel, Field

# LOCAL LIBRARY IMPORTS


class BlogPostModel(BaseModel):
    """
    A pydantic model for the blog post
    """

    post_name: str = Field(
        ..., max_length=256, description="The name of the blog post, unique"
    )
    description: str = Field(
        ..., max_length=50, description="A short description of the blog post"
    )
    text: str = Field(..., description="The full text of the blog post")
    released: bool = Field(
        default=False, description="Flag indicating if the blog post is released"
    )


class BlogPostFilterModel(BaseModel):
    """
    A pydantic model for filtering blog post
    """

    post_name: str = Field(None, description="The name of the blog post")
    description: str = Field(
        None,
        description="A short description of the blog post does not need to be exact",
    )
    text: str = Field(None, description="Text to search for in the blog post")
    released: bool = Field(
        None, description="Flag indicating if the blog post is released"
    )
