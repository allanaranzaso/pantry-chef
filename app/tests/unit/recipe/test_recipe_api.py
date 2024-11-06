from typing import Any
from unittest.mock import (
    ANY,
    Mock,
)

import pytest
from fastapi import status
from httpx import AsyncClient

from pantry_chef.recipe.exceptions import (
    DBRecipeCreationFailed,
)
from pantry_chef.recipe.schema import RecipeSchema


@pytest.fixture
def recipe_endpoint():
    return '/api/v1/recipe/'


@pytest.fixture
def mock_get_recipe(
    mocker: Mock,
    recipe_schema: RecipeSchema,
) -> Mock:
    mock = mocker.patch('pantry_chef.recipe.api.db_get_recipe_by_uuid')
    mock.return_value = recipe_schema

    return mock


@pytest.fixture
def mock_create_recipe(
    recipe_schema: RecipeSchema,
    mocker: Mock,
) -> Mock:
    mock = mocker.patch('pantry_chef.recipe.api.db_create_recipe')
    mock.return_value = recipe_schema

    return mock


@pytest.fixture
def mock_update_recipe(
    recipe_schema: RecipeSchema,
    mocker: Mock,
) -> Mock:
    mock = mocker.patch('pantry_chef.recipe.api.db_update_recipe')
    mock.return_value = recipe_schema

    return mock


@pytest.fixture
def valid_recipe_dict(
    recipe_schema: RecipeSchema,
) -> dict[str, Any]:
    return recipe_schema.model_dump(mode='json', by_alias=True)


@pytest.mark.asyncio
async def test_post_create_recipe(
    mock_create_recipe: Mock,
    client: AsyncClient,
    recipe_endpoint: str,
    valid_recipe_dict: dict[str, Any],
    recipe_schema: RecipeSchema,
):
    response = await client.post(
        recipe_endpoint,
        json=valid_recipe_dict,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == valid_recipe_dict
    mock_create_recipe.assert_called_once_with(
        db=ANY,
        recipe=recipe_schema,
    )


@pytest.mark.asyncio
async def test_post_create_recipe_raises_400(
    mock_create_recipe: Mock,
    client: AsyncClient,
    recipe_endpoint: str,
    valid_recipe_dict: dict[str, Any],
    recipe_schema: RecipeSchema,
):
    mock_create_recipe.side_effect = DBRecipeCreationFailed(Exception('Test exception'))

    response = await client.post(
        recipe_endpoint,
        json=valid_recipe_dict,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': ['Test exception']}
    mock_create_recipe.assert_called_once_with(
        db=ANY,
        recipe=recipe_schema,
    )


@pytest.mark.asyncio
async def test_get_recipe_by_uuid(
    mock_get_recipe: Mock,
    client: AsyncClient,
    recipe_endpoint: str,
    valid_recipe_dict: dict[str, Any],
    recipe_schema: RecipeSchema,
):
    response = await client.get(f'{recipe_endpoint}{recipe_schema.uuid}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == valid_recipe_dict
    mock_get_recipe.assert_called_once_with(
        db=ANY,
        uuid=recipe_schema.uuid,
    )


@pytest.mark.asyncio
async def test_put_update_recipe(
    mock_update_recipe: Mock,
    client: AsyncClient,
    recipe_endpoint: str,
    valid_recipe_dict: dict[str, Any],
    recipe_schema: RecipeSchema,
):
    response = await client.put(
        f'{recipe_endpoint}{recipe_schema.uuid}',
        json=valid_recipe_dict,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == valid_recipe_dict
    mock_update_recipe.assert_called_once_with(
        db=ANY,
        uuid=recipe_schema.uuid,
        recipe=recipe_schema,
    )


@pytest.mark.asyncio
async def test_put_update_recipe_raises_400(
    mock_update_recipe: Mock,
    client: AsyncClient,
    recipe_endpoint: str,
    valid_recipe_dict: dict[str, Any],
    recipe_schema: RecipeSchema,
):
    mock_update_recipe.side_effect = DBRecipeCreationFailed(ValueError('Test exception'))

    response = await client.put(
        f'{recipe_endpoint}{recipe_schema.uuid}',
        json=valid_recipe_dict,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': ['Test exception']}
    mock_update_recipe.assert_called_once_with(
        db=ANY,
        uuid=recipe_schema.uuid,
        recipe=recipe_schema,
    )
