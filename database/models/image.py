"""
file_name = image.py
Created On: 2024/07/09
Lasted Updated: 2024/07/09
Description: _FILL OUT HERE_
Edit Log:
2024/07/09
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from sqlalchemy import Boolean, String, LargeBinary
from sqlalchemy.orm import mapped_column, Mapped

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS
from database.database import BASE
from src.models.image_model import ImageModel


class Image(BASE):
    """
    A model class for the images table
    """

    __tablename__ = "images"

    image_name: Mapped[str] = mapped_column(
        String, primary_key=True, unique=True, nullable=False
    )
    image_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    released: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __init__(self, image: ImageModel):
        self.image_name = image.image_name
        self.image_data = image.image_data
        self.released = image.released
