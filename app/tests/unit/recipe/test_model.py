import pytest


@pytest.fixture
def recipe():
    return Recipe(name='Pasta Carbonara', description='Italian pasta dish')
