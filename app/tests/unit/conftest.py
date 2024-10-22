import pytest

from pantry_chef.ingredient.schema import IngredientSchema, UOMEnum
from pantry_chef.instruction.schema import InstructionSchema
from pantry_chef.recipe.schema import RecipeSchema


@pytest.fixture
def instruction_schema():
    return InstructionSchema(
        step_number='1',
        description='Thaw chicken',
    )


@pytest.fixture
def ingredient_schema():
    return IngredientSchema(
        name='Chicken',
        quantity=1,
        uom=UOMEnum.LB,
    )


@pytest.fixture
def recipe_schema():
    return RecipeSchema(
        name='Chicken Alfredo',
        description='A creamy pasta dish with chicken',
        cuisine_type='Italian',
    )
