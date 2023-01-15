import threading

from abc import ABC

from noted.database import Database


class BaseRecipe(ABC):
    """Starting point of any Noted workflow. It defines what the next task is."""

    def __init__(self, database: Database) -> None:
        super().__init__()

    def get_next_task(self):
        pass

    def get_config(self):
        pass


class RecipeManager:
    def __init__(self, recipe: BaseRecipe) -> None:
        self._recipe = recipe
        self._current_task = self._recipe.get_next_task()

        # Used for syncronizing the advance method.
        # need this because our task arrive in a sequence.
        self._lock = threading.Lock()

    def config(self):
        return self._recipe.get_config()

    def advance(self):
        with self._lock:
            self._current_task = self._recipe.get_next_task()

    def result(self, data):
        print("RESULT", data)

    def current(self):
        return self._current_task
