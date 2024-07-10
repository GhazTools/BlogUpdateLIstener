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
    IGNORE_FOLDERS: Final[list[str]] = [".git", ".obsidian"]

    def __init__(self: "VaultReader") -> None:
        self.image_data: Images = self._extract_image_data()
        self.blog_posts: BlogPosts = []

    # PRIVATE METHODS START HERE

    def _extract_image_data(self: "VaultReader") -> Images:
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

    def _extract_blog_posts(self: "VaultReader") -> BlogPosts:
        """
        Extracts all blog posts from the vault
        """

        image_dir_path: Path = Path(self.VAULT_PATH) / "__BLOG_POSTS__"
        blog_posts: BlogPosts = []

        for object_path in image_dir_path.iterdir():
            # Each blog post is a directory
            if object_path.is_file():
                continue

            post_name: str = object_path.name
            description: str = self._get_post_description(object_path)
            text: str = self._get_post_text(object_path)
            released = False  # TODO: Check db for existance & check if released in db

            blog_post: BlogPostModel = BlogPostModel(
                post_name=post_name,
                description=description,
                text=text,
                released=released,
            )

            blog_posts.append(blog_post)

        return blog_posts

    def _get_post_description(self: "VaultReader", post_path: Path) -> str:
        """
        Extracts the description of a blog post
        """

        description_path: Path = post_path / "description.md"

        if not description_path.exists():
            raise ValueError(f"Description file for {post_path.name} does not exist")

        with open(description_path, "r", encoding="UTF-8") as description_file:
            description: str = description_file.read()

        if len(description) > 50:
            raise ValueError(
                f"Description for {post_path.name} is too long, max length is 50 characters"
            )

        return description

    def _get_post_text(self: "VaultReader", post_path: Path) -> str:
        """
        Extracts the text of a blog post
        """

        text_path: Path = post_path / "text.md"

        if not text_path.exists():
            raise ValueError(f"Text file for {post_path.name} does not exist")

        with open(text_path, "r", encoding="UTF-8") as text_file:
            text: str = text_file.read()

        return text

    # PRIVATE METHODS END HERE
