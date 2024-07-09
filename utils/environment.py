"""
file_name = environment.py
Created On: 2024/07/09
Lasted Updated: 2024/07/09
Description: _FILL OUT HERE_
Edit Log:
2024/07/09
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from enum import Enum
from pathlib import Path

# THIRD PARTY LIBRARY IMPORTS
from environment_loader.environment import Environment

# LOCAL LIBRARY IMPORTS


class EnvironmentVariableKeys(Enum):
    """
    Enum class for environment variable keys
    """

    DATABASE_URL = "DATABASE_URL"


# Only runs on first import
Environment.setup_environment(
    EnvironmentVariableKeys,  # Keys
    Path(__file__).resolve().parents[1] / ".env",  # Path to env file, in project root
)
