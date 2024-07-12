"""
file_name = image_blueprint.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from sanic import Blueprint, Request
from sanic.response import HTTPResponse, json
from pydantic import ValidationError

# LOCAL LIBRARY IMPORTS
from src.database.models.image import Image
from src.database.repositories.image_repository import ImageRepository

from src.models.image_model import (
    ImageFilterModel,
    ImageReleaseUpdateRequest,
    ImageReleasePublishRequest,
    ImageStatusRequest,
    ImageStatusResponse,
)

from src.utils.vault_reader import VaultReader
from src.utils.logger import AppLogger


IMAGES_BLUEPRINT = Blueprint("image_blueprint", url_prefix="/images")


@IMAGES_BLUEPRINT.route("/<image_name>", methods=["GET"])
async def base_route(
    _request: Request,
    image_name: str,
) -> HTTPResponse:
    """
    Gets images from the database that have been released
    """
    image: Image | None = None

    with ImageRepository() as repository:
        image_filters: ImageFilterModel = ImageFilterModel(
            image_name=image_name, released=True
        )
        images: list[Image] = repository.get_images(image_filters)

        if not images:
            return HTTPResponse("Image not found", status=404)

        image = images[0]

    mime_type = "image/jpeg" if image.image_name.endswith(".jpg") else "image/png"
    return HTTPResponse(body=image.image_data, content_type=mime_type)


@IMAGES_BLUEPRINT.route("/imageStatus", methods=["POST"])
async def get_image_status(request: Request) -> HTTPResponse:
    """
    Checks if an image is published
    
    """
    logger = AppLogger.get_logger()
    
    try:
        image_status_request: ImageStatusRequest = ImageStatusRequest(**request.json)
    except ValidationError as e:
        logger.info("Could not valid image status request %s", e)
        return HTTPResponse("Invalid request body", status=400)

    published = False
    released = False

    with ImageRepository() as repository:
        image_filters: ImageFilterModel = ImageFilterModel(
            image_name=image_status_request.image_name, released=None
        )
        images: list[Image] = repository.get_images(image_filters)
        
        if images:
            published = True
            released = images[0].released

    return json(ImageStatusResponse(published=published, released=released).json())


@IMAGES_BLUEPRINT.route("/publish", methods=["POST"])
async def publish_image(request: Request) -> HTTPResponse:
    """
    Publishes an image
    """
    try:
        image_publish_request: ImageReleasePublishRequest = ImageReleasePublishRequest(
            **request.json
        )
    except ValidationError:
        return HTTPResponse("Invalid request body", status=400)

    vault_reader: VaultReader = request.app.config["VAULT_READER"]
    image_found: bool = False

    for image in vault_reader.images_to_add:
        if image.image_name == image_publish_request.image_name:
            with ImageRepository() as repository:
                repository.insert_image(image)

            image_found = True
            break

    if not image_found:
        return HTTPResponse("Image not found", status=404)

    return HTTPResponse("Image published", status=200)


@IMAGES_BLUEPRINT.route("/getImage", methods=["POST"])
async def get_image(request: Request) -> HTTPResponse:
    """
    Gets images from the database that have been released

    Filtering requires auth
    """
    try:
        image_filters: ImageFilterModel = ImageFilterModel(**request.json)
    except ValidationError:
        return HTTPResponse("Invalid request body", status=400)

    images: list[Image] | None = None

    with ImageRepository() as repository:
        images = repository.get_images(image_filters)

        if not images:
            return HTTPResponse("Image not found", status=404)

    return json(
        {
            "images": [image.to_model().json() for image in images],
        }
    )


@IMAGES_BLUEPRINT.route("/updateImageRelease", methods=["POST"])
async def update_image_release(request: Request) -> HTTPResponse:
    """
    Updates the release status of an image
    """
    logger = AppLogger.get_logger()
    
    try:
        image_release_update_request: ImageReleaseUpdateRequest = ImageReleaseUpdateRequest(**request.json)
    except ValidationError:
        logger.info("Could not valid update image release request %s", e)
        return HTTPResponse("Invalid request body", status=400)
        

    with ImageRepository() as repository:
        try:
            repository.update_release(image_release_update_request.image_name, image_release_update_request.release)
        except ValueError:
            logger.info("Could not find image %s", image_release_update_request.image_name)
            return HTTPResponse("Image not found", status=404)

    return HTTPResponse("Image release status updated", status=200)
