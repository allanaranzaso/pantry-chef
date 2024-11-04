from enum import Enum
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

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, value: float) -> float:
        if value <= 0:
            raise ValueError('Quantity must be a positive number')
        return value

    @field_validator('uom')
    @classmethod
    def validate_uom(cls, value: str) -> str:
        if not value:
            raise ValueError('Unit of measure must not be empty')

        if value not in UOMEnum:
            raise ValueError('Invalid unit of measure')

        return value
