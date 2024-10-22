from typing import Annotated, List
from uuid import UUID, uuid4

from annotated_types import Predicate
from pydantic import Field, field_validator

from pantry_chef.base_schema import BaseSchema, BaseStatusSchema, BaseTelemetrySchema
from pantry_chef.validators import is_not_empty_string


class RecipeSchema(BaseSchema, BaseStatusSchema, BaseTelemetrySchema):
    uuid: UUID = Field(default_factory=uuid4)
    name: Annotated[str, Predicate(is_not_empty_string)]
    description: str = ''
    ingredient_uuids: List[UUID] = []
    instruction_uuids: List[UUID] = []
    cuisine_type: str = ''

    @field_validator('ingredient_uuids')
    def validate_ingredient_uuids(cls, value):
        for uuid in value:
            if not isinstance(uuid, UUID):
                raise ValueError(f'Invalid ingredient UUID: {uuid}')

        return value

    @field_validator('instruction_uuids')
    def validate_instruction_uuids(cls, value):
        for uuid in value:
            if not isinstance(uuid, UUID):
                raise ValueError(f'Invalid instruction UUID: {uuid}')

        return value
