import uvicorn
import uvicorn.config

from noted.database import Database
from noted.server import create_server
from noted.recipe import BaseRecipe, RecipeManager


def run_recipe(recipe: BaseRecipe, task_name: str):
    ## Preparation
    database = Database()

    ## Initialization
    manager = RecipeManager(recipe, database, config={"task_name": task_name})

    ## Run the server
    app = create_server(manager)
    config = uvicorn.Config(app, port=8000, log_level=uvicorn.config.LOG_LEVELS['critical'])

    server = uvicorn.Server(config)
    server.run()
