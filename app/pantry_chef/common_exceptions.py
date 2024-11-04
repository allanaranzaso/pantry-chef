from typing import (
    Any,
    Tuple,
)


class CustomValidationError(Exception):
    detail: Tuple[Any, ...]

    def __init__(self, error_msg: str | list[Any]) -> None:
        if isinstance(error_msg, str):
            error_msg = [{'error': error_msg}]
        self.detail = tuple(error_msg)
