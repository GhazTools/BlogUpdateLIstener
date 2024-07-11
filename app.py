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
from src.database.repositories.image_repository import ImageRepository


APP_INSTANTIATOR = AppInstantiator()
app: Sanic = APP_INSTANTIATOR.app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    # vault_reader = app.config["VAULT_READER"]
    # print(vault_reader)

    # images = vault_reader.images_to_add

    # print(images)

    # with ImageRepository() as image_repo:
    #     for image in images:
    #         image_repo.insert_image(image)
