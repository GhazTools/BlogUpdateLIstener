"""
file_name = image_blueprint_model.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from pydantic import BaseModel

# LOCAL LIBRARY IMPORTS


class GetImageModelResponse(BaseModel):
    """
    A pydantic model for getting an image
    """

    image_data: bytes
