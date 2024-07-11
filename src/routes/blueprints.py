"""
file_name = blueprints.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from typing import Final

# THIRD PARTY LIBRARY IMPORTS
from sanic import Blueprint
from sanic.request import Request
from sanic.response import text, HTTPResponse

# LOCAL LIBRARY IMPORTS
from src.routes.image_blueprint import IMAGES_BLUEPRINT
from src.routes.blog_posts_model import BLOG_POSTS_BLUEPRINT


ENTRY_POINT_BLUEPRINT = Blueprint("entry_point_blueprint", url_prefix="/")


@ENTRY_POINT_BLUEPRINT.get("/")
async def entry_point(_request: Request) -> HTTPResponse:
    """
    A request to validate that the app is running
    """

    return text("App is currently running.")


BLUEPRINTS: Final[list[Blueprint]] = [
    ENTRY_POINT_BLUEPRINT,
    IMAGES_BLUEPRINT,
    BLOG_POSTS_BLUEPRINT,
]
