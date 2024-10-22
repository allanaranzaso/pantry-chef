from uuid import UUID

import pytest

from pantry_chef.ingredient.schema import IngredientSchema


def test_ingredient_valid_schema(ingredient_schema: IngredientSchema) -> None:
    valid_ingredient_schema = ingredient_schema.model_dump()

    assert IngredientSchema.model_validate(valid_ingredient_schema)


@pytest.mark.parametrize(
    ('field', 'invalid_value'),
    [
        ('name', 1),
        ('quantity', ''),
        ('quantity', -1),
        ('uom', ''),
        ('uom', 'Invalid value'),
        ('recipes', ''),
        ('recipes', ['invalid']),
    ],
)
def test_ingredient_invalid_schema(
        field: str,
        invalid_value: str,
        ingredient_schema: IngredientSchema
) -> None:
    invalid_ingredient_schema = ingredient_schema.model_dump()
    invalid_ingredient_schema[field] = invalid_value
    error_msg = rf'1 validation error for.+\n{field}(\.0)?\n.+'

    with pytest.raises(ValueError, match=error_msg):
        IngredientSchema.model_validate(invalid_ingredient_schema)


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('Chicken', 'Chicken'),
    ]
)
def test_ingredient_schema_default_value(value: str, expected: str) -> None:
    ingredient_schema = IngredientSchema(name=value)

    assert isinstance(ingredient_schema.uuid, UUID)
    assert ingredient_schema.name == expected
    assert ingredient_schema.quantity == 0
    assert ingredient_schema.uom == 'each'
    assert ingredient_schema.recipes == []
