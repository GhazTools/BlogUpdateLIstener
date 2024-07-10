"""
file_name = app_instantiator.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from logging import Logger

# THIRD PARTY LIBRARY IMPORTS
from sanic import Sanic

# LOCAL LIBRARY IMPORTS
from src.routes.blueprints import BLUEPRINTS

from src.utils.logger import AppLogger
from src.utils.middleware import Middleware
from src.utils.vault_reader import VaultReader
from src.utils.tasks import task_reload_vault_reader


class AppInstantiator:
    """
    A class to instantiate the sanic applicaiton
    """

    def __init__(self: "AppInstantiator") -> None:
        self._app = Sanic("BlogUpdaterSvc")

        logger: Logger = AppLogger.get_logger()
        logger.info("Attempting to start the application")

        # Register objects
        self._register_globals()
        self._register_middleware()
        self._register_blueprints()
        self._register_tasks()

        logger.info("Finished setting up the applicaiton")

    # PROPERTIES START HERE

    @property
    def app(self: "AppInstantiator") -> Sanic:
        """
        A function retrieve the app
        """

        return self._app

    # PROPERTIES END HERE

    # PUBLIC METHODS START HERE
    # PUBLIC METHODS END HERE

    # PRIVATE METHODS START HERE
    def _register_globals(self: "AppInstantiator") -> None:
        self.app.config["MIDDLEWARE"] = Middleware()
        self.app.config["VAULT_READER"] = VaultReader()

    def _register_middleware(self: "AppInstantiator") -> None:
        middleware: Middleware = self.app.config["MIDDLEWARE"]

        self.app.register_middleware(middleware.request_middleware, "request")
        self.app.register_middleware(middleware.response_middleware, "response")

    def _register_blueprints(self: "AppInstantiator") -> None:
        for blueprint in BLUEPRINTS:
            self.app.blueprint(blueprint)

    def _register_tasks(self: "AppInstantiator") -> None:
        self.app.add_task(task_reload_vault_reader(self.app))

    # PRIVATE METHODS END HERE
