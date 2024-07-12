"""
file_name = vault_blueprint.py
Created On: 2024/07/12
Lasted Updated: 2024/07/12
Description: _FILL OUT HERE_
Edit Log:
2024/07/12
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from subprocess import run, CalledProcessError

# THIRD PARTY LIBRARY IMPORTS
from sanic import Blueprint, Request
from sanic.response import HTTPResponse, text

# LOCAL LIBRARY IMPORTS
from src.utils.environment import Environment, EnvironmentVariableKeys
from src.utils.vault_reader import VaultReader
from src.utils.logger import AppLogger

VAULT_BLUEPRINT = Blueprint("vault_blueprint", url_prefix="/vault")



@VAULT_BLUEPRINT.post("/sync")
async def sync_vault(request: Request) -> HTTPResponse:
    """
    A request to sync the vault
    """
    logger = AppLogger.get_logger()
    
    vault_path: str = Environment.get_environment_variable(
        EnvironmentVariableKeys.VAULT_PATH
    )
    
    try:
        run(["git", "-C", vault_path, "pull"], check=True)
        vault_reader: VaultReader = request.app.config["VAULT_READER"]
        vault_reader.reload_vault_reader()
        
        logger.info("Successfully synced repo")
    except Exception as e:
        logger.info("Failed to sync with %s", e)

    return text("Successfully synced vault.")
