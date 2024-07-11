"""
file_name = blog_posts_model.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from sanic import Blueprint, Request
from sanic.response import HTTPResponse
# from pydantic import ValidationError


# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS
from src.database.models.blog_post import BlogPost
from src.database.repositories.blog_post_repository import BlogPostRepository

from src.models.blog_post_model import BlogPostFilterModel


BLOG_POSTS_BLUEPRINT = Blueprint("blog_posts_blueprint", url_prefix="/blogPosts")


@BLOG_POSTS_BLUEPRINT.get("/<post_namee>", methods=["GET"])
async def base_route(
    _request: Request,
    post_name: str,
) -> HTTPResponse:
    """
    Gets blog posts fro mteh database that have been released
    """

    blog_post: BlogPost | None = None

    with BlogPostRepository() as repository:
        blog_posts_filter: BlogPostFilterModel = BlogPostFilterModel(
            post_name=post_name, description=None, text=None, released=True
        )

        blog_posts: list[BlogPost] = repository.get_blog_posts(blog_posts_filter)

        if not blog_posts:
            return HTTPResponse("Blog post not found", status=404)

        blog_post = blog_posts[0]

    return HTTPResponse(body=blog_post.json(), content_type="application/json")
