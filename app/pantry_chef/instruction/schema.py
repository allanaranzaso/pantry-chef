from typing import Annotated, List
from uuid import UUID, uuid4

from annotated_types import Predicate
from pydantic import field_validator, field_serializer, Field

from pantry_chef.base_schema import BaseSchema, BaseStatusSchema, BaseTelemetrySchema
from pantry_chef.validators import is_not_empty_string


class InstructionSchema(BaseSchema, BaseStatusSchema, BaseTelemetrySchema):
    uuid: UUID = Field(default_factory=uuid4)
    recipe_uuids: List[UUID] = []
    step_number: str = '1'
    description: Annotated[str, Predicate(is_not_empty_string)]
    duration_ms: int = 0

    @field_validator('step_number')
    def validate_step_number(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError('Step number must be a digit')
        return value

    @field_validator('duration_ms')
    def validate_duration_ms(cls, value: int | str) -> int:
        if value < 0:
            raise ValueError('Duration must be a positive number')

        if isinstance(value, str):
            raise ValueError('Duration must be a number')

        return value

    @field_validator('recipe_uuids')
    def validate_recipe_uuids(cls, value: List[UUID]) -> List[UUID]:
        for uuid in value:
            if not isinstance(uuid, UUID):
                raise ValueError('Invalid recipe UUID')

        return value

    @field_serializer('recipe_uuids')
    def serialize_recipe_uuids(self, value: List[UUID]) -> List[str]:
        return [str(uuid) for uuid in value]
