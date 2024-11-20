from uuid import UUID

from pantry_chef.recipe.schema import RecipeSchema


def test_recipe_valid_schema(recipe_schema: RecipeSchema) -> None:
    valid_recipe_schema = recipe_schema.model_dump()

    assert RecipeSchema.model_validate(valid_recipe_schema)


def test_recipe_default_values() -> None:
    recipe = RecipeSchema(name='Test')

    assert isinstance(recipe.uuid, UUID)
    assert recipe.description == ''
    assert recipe.cuisine_type == ''
    assert recipe.ingredients_uuids == []
    assert recipe.instructions_uuids == []
