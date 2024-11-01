from typing import Annotated
from uuid import UUID, uuid4

from annotated_types import Predicate
from pydantic import Field

from pantry_chef.base_schema import BaseSchema, BaseStatusSchema, BaseTelemetrySchema
from pantry_chef.validators import is_not_empty_string


class RecipeSchema(BaseSchema, BaseStatusSchema, BaseTelemetrySchema):
    uuid: UUID = Field(default_factory=uuid4)
    name: Annotated[str, Predicate(is_not_empty_string)]
    description: str = ''
    ingredient_uuids: list[UUID] = []
    instruction_uuids: list[UUID] = []
    cuisine_type: str = ''
