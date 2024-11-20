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
    ingredients_uuids: list[UUID] = Field(default_factory=list)
    instructions_uuids: list[UUID] = Field(default_factory=list)
    cuisine_type: str = ''
