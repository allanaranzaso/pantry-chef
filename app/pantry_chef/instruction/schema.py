from typing import Annotated
from uuid import (
    UUID,
    uuid4,
)

from annotated_types import Predicate
from pydantic import (
    Field,
    field_validator,
)

from pantry_chef.base_schema import (
    BaseSchema,
    BaseStatusSchema,
    BaseTelemetrySchema,
)
from pantry_chef.validators import is_not_empty_string


class InstructionSchema(BaseSchema, BaseStatusSchema, BaseTelemetrySchema):
    uuid: UUID = Field(default_factory=uuid4)
    step_number: str = '1'
    description: Annotated[str, Predicate(is_not_empty_string)]
    duration_ms: int = 0

    @field_validator('step_number')
    @classmethod
    def validate_step_number(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError('Step number must be a digit')
        return value

    @field_validator('duration_ms')
    @classmethod
    def validate_duration_ms(cls, value: int | str) -> int:
        if isinstance(value, int) and value < 0:
            raise ValueError('Duration must be a positive number')

        if isinstance(value, str):
            raise ValueError('Duration must be a number')

        return value
