"""
file_name = vault_reader.py
Created On: 2024/07/09
Lasted Updated: 2024/07/09
Description: _FILL OUT HERE_
Edit Log:
2024/07/09
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from pathlib import Path
from typing import Final

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS
from src.models.image_model import ImageModel
from src.models.blog_post_model import BlogPostModel
from utils.environment import Environment, EnvironmentVariableKeys

Images = list[ImageModel]
BlogPosts = list[BlogPostModel]


class VaultReader:
    """
    A class for reading an obsidian vault to manage blog posts
    """

    VAULT_PATH: Final[str] = Environment.get_environment_variable(
        EnvironmentVariableKeys.VAULT_PATH
    )

    def __init__(self: "VaultReader") -> None:
        self.image_data: Images = []
        self.blog_posts: BlogPosts = []

    def extract_image_data(self: "VaultReader") -> Images:
        """
        Extracts all images from the vault
        """

        image_dir_path: Path = Path(self.VAULT_PATH) / "__IMAGES__"
        images: Images = []

        for object_path in image_dir_path.iterdir():
            if not self._validate_image_path(object_path):
                continue

            with open(object_path, "rb") as image_file:
                image_name: str = object_path.name
                image_data: bytes = image_file.read()
                released = (
                    False  # TODO: Check db for existance & check if released in db
                )

                image: ImageModel = ImageModel(
                    image_name=image_name, image_data=image_data, released=released
                )

                images.append(image)

        return images

    def _validate_image_path(self, object_path: Path) -> bool:
        """
        Validates that the image path is a valid image
        """

        # TODO: Currently only supports png

        if not object_path.is_file():
            return False

        if not object_path.name.endswith(".png"):
            return False

        return True
