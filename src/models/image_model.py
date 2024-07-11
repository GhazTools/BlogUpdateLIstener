"""
file_name = image_model.py
Created On: 2024/07/09
Lasted Updated: 2024/07/09
Description: _FILL OUT HERE_
Edit Log:
2024/07/09
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from typing import Optional

# THIRD PARTY LIBRARY IMPORTS
from pydantic import BaseModel, Field

# LOCAL LIBRARY IMPORTS


class ImageModel(BaseModel):
    """
    A pydantic model for images
    """

    image_name: str = Field(..., description="The name of the image")
    image_data: bytes = Field(..., description="The binary data of the image")
    released: bool = Field(
        default=False, description="Flag indicating if the image is released"
    )


class ImageFilterModel(BaseModel):
    """
    A pydantic model for filtering images
    """

    image_name: Optional[str] = Field(None, description="The name of the image")
    released: Optional[bool] = Field(
        None, description="Flag indicating if the image is released"
    )
