"""
file_name = blog_posts_blueprint.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from sanic import Blueprint, Request
from sanic.response import HTTPResponse, json
from pydantic import ValidationError


# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS
from src.database.models.blog_post import BlogPost
from src.database.repositories.blog_post_repository import BlogPostRepository

from src.models.blog_post_model import BlogPostFilterModel, BlogPostReleaseUpdateRequest


BLOG_POSTS_BLUEPRINT = Blueprint("blog_posts_blueprint", url_prefix="/blogPosts")


@BLOG_POSTS_BLUEPRINT.get("/<post_namee>")
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

    return HTTPResponse(
        body=blog_post.to_model().json(), content_type="application/json"
    )


@BLOG_POSTS_BLUEPRINT.route("/getBlogPost", methods=["POST"])
async def get_blog_post(request: Request) -> HTTPResponse:
    """
    Gets blog posts from the database that have been released

    Filtering requires auth
    """
    try:
        blog_post_filters: BlogPostFilterModel = BlogPostFilterModel(**request.json)
    except ValidationError as error:
        return HTTPResponse(f"Error: {error}", status=400)

    with BlogPostRepository() as repository:
        blog_posts: list[BlogPost] = repository.get_blog_posts(blog_post_filters)

        if not blog_posts:
            return HTTPResponse("Blog post not found", status=404)

    return json(
        {
            "blog_posts": [blog_post.to_model().json() for blog_post in blog_posts],
        }
    )


@BLOG_POSTS_BLUEPRINT.route("/updatePostRelease", methods=["POST"])
async def update_post_release(request: Request) -> HTTPResponse:
    """
    Updates the release status of a blog post
    """
    try:
        update_request: BlogPostReleaseUpdateRequest = BlogPostReleaseUpdateRequest(
            **request.json
        )
    except ValidationError as error:
        return HTTPResponse(f"Error: {error}", status=400)

    with BlogPostRepository() as repository:
        repository.update_release(update_request.post_name, update_request.release)

    return HTTPResponse("Blog post release status updated", status=200)
