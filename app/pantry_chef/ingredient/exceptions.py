import json
from typing import Any

from pydantic import ValidationError


class DBIngredientCreationFailed(Exception):
    detail: tuple[Any, ...]

    def __init__(self, db_err: Exception) -> None:
        self.detail = db_err.args
        if not self.detail and isinstance(db_err, ValidationError):
            self.detail = json.loads(db_err.json())


class DBIngredientUpdateFailed(Exception):
    detail: tuple[Any, ...]

    def __init__(self, db_err: Exception) -> None:
        self.detail = db_err.args
        if not self.detail and isinstance(db_err, ValidationError):
            self.detail = json.loads(db_err.json())


class IngredientNotFoundException(Exception):
    pass
