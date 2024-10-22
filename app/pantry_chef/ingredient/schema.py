from enum import Enum
from typing import Annotated, List
from uuid import UUID, uuid4

from annotated_types import Predicate
from pydantic import Field, field_serializer, field_validator

from pantry_chef.base_schema import BaseSchema, BaseStatusSchema, BaseTelemetrySchema
from pantry_chef.validators import is_not_empty_string


class UOMEnum(str, Enum):
    CUP = 'cup'
    FL_OZ = 'fluid_ounce'
    GAL = 'gallon'
    OZ = 'ounce'
    PINT = 'pint'
    LB = 'pound'
    QT = 'quart'
    TBSP = 'tablespoon'
    TSP = 'teaspoon'
    L = 'liter'
    EACH = 'each'
    DASH = 'dash'
    PINCH = 'pinch'
    TASTE = 'to taste'


class IngredientSchema(BaseSchema, BaseStatusSchema, BaseTelemetrySchema):
    uuid: UUID = Field(default_factory=uuid4)
    name: Annotated[str, Predicate(is_not_empty_string)]
    quantity: float = 0
    uom: UOMEnum = UOMEnum.EACH
    recipes: List[UUID] = []

    @field_validator('quantity')
    def validate_quantity(cls, value: float) -> float:
        if value <= 0:
            raise ValueError('Quantity must be a positive number')
        return value

    @field_validator('uom')
    def validate_uom(cls, value: str) -> str:
        if not value:
            raise ValueError('Unit of measure must not be empty')

        if value not in UOMEnum:
            raise ValueError('Invalid unit of measure')

        return value

    @field_validator('recipes')
    def validate_recipes(cls, value: List[UUID]) -> List[UUID]:
        for uuid in value:
            if not isinstance(uuid, UUID):
                raise ValueError('Invalid recipe UUID')

        return value

    @field_serializer('recipes')
    def serialize_recipes(self, value: List[UUID]) -> List[str]:
        return [str(uuid) for uuid in value]
