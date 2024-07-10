"""
file_name = base_request_model.py
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


class BaseRequest(BaseModel):
    """
    A base class for base requests to the service
    """

    user: str
    token: str
