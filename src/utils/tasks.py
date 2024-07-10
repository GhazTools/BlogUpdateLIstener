"""
file_name = tasks.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from asyncio import sleep
from sanic import Sanic

# LOCAL LIBRARY IMPORTS
from src.utils.vault_reader import VaultReader


async def task_reload_vault_reader(app: Sanic) -> None:
    """
    Reload vault task, runs every 30 minutes
    """

    await sleep(60 * 30)  # Run every 30 minutes

    vault_reader: VaultReader = app.config["VaultReader"]
    vault_reader.reload_vault_reader()  # TODO: Optimize
