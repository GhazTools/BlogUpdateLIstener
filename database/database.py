"""
file_name = database.py
Created On: 2024/07/09
Lasted Updated: 2024/07/09
Description: _FILL OUT HERE_
Edit Log:
2024/07/09
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine.base import Engine

# LOCAL LIBRARY IMPORTS
from utils.environment import Environment, EnvironmentVariableKeys


def get_engine() -> Engine:
    """
    Creates and returns an SQLAlchemy engine object.

    This function reads environment variables for the connection details to the
    database and uses them to create an SQLAlchemy engine object.

    Returns:
        An SQLAlchemy engine object that can be used to connect to a database.
    """

    engine: Engine = create_engine(
        Environment.get_environment_variable(EnvironmentVariableKeys.DATABASE_URL),
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
    )

    return engine


ENGINE: Engine = get_engine()
BASE = declarative_base()
SESSION_MAKER = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
