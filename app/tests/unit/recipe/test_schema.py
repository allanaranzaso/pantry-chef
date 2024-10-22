from uuid import UUID

import pytest

from pantry_chef.recipe.schema import RecipeSchema


def test_recipe_valid_schema(recipe_schema: RecipeSchema) -> None:
    valid_recipe_schema = recipe_schema.model_dump()

    assert RecipeSchema.model_validate(valid_recipe_schema)


@pytest.mark.parametrize(
    ('field', 'invalid_value'),
    [
        ('ingredient_uuids', ['invalid value']),
        ('instruction_uuids', ['invalid value']),
    ],
)
def test_recipe_invalid_schema_raises_value_error(
        field: str,
        invalid_value: str,
        recipe_schema: RecipeSchema
) -> None:
    invalid_recipe_schema = recipe_schema.model_dump()
    invalid_recipe_schema[field] = invalid_value
    error_msg = rf'1 validation error for.+\n{field}(\.0)?\n.+'

    with pytest.raises(ValueError, match=error_msg):
        RecipeSchema.model_validate(invalid_recipe_schema)


def test_recipe_default_values() -> None:
    recipe = RecipeSchema(name='Test')

    assert isinstance(recipe.uuid, UUID)
    assert recipe.description == ''
    assert recipe.cuisine_type == ''
    assert recipe.ingredient_uuids == []
    assert recipe.instruction_uuids == []
