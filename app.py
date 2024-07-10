"""
file_name = app.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from sanic import Sanic

# LOCAL LIBRARY IMPORTS
from src.app_instantiator import AppInstantiator


APP_INSTANTIATOR = AppInstantiator()
app: Sanic = APP_INSTANTIATOR.app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
