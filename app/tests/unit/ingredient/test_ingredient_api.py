from typing import Any
from unittest.mock import (
    ANY,
    Mock,
)
from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from pantry_chef.ingredient.exceptions import (
    DBIngredientCreationFailed,
)
from pantry_chef.ingredient.schema import IngredientSchema


@pytest.fixture
def ingredient_endpoint():
    return '/api/v1/ingredient/'


@pytest.fixture
def mock_get_ingredient(
    mocker: Mock,
    ingredient_schema: IngredientSchema,
) -> Mock:
    mock = mocker.patch('pantry_chef.ingredient.api.get_ingredient_by_uuid')
    mock.return_value = ingredient_schema

    return mock


@pytest.fixture
def mock_create_ingredient(
    ingredient_schema: IngredientSchema,
    mocker: Mock,
) -> Mock:
    mock = mocker.patch('pantry_chef.ingredient.api.create_ingredient')
    mock.return_value = ingredient_schema

    return mock


@pytest.fixture
def mock_update_ingredient(
    ingredient_schema: IngredientSchema,
    mocker: Mock,
) -> Mock:
    mock = mocker.patch('pantry_chef.ingredient.api.update_ingredient')
    mock.return_value = ingredient_schema

    return mock


@pytest.fixture
def valid_ingredient_dict(
    ingredient_schema: IngredientSchema,
) -> dict[str, Any]:
    return ingredient_schema.model_dump(mode='json', by_alias=True)


@pytest.mark.asyncio
async def test_post_create_ingredient(
    mock_create_ingredient: Mock,
    client: AsyncClient,
    ingredient_endpoint: str,
    valid_ingredient_dict: dict[str, Any],
    ingredient_schema: IngredientSchema,
) -> None:
    response = await client.post(
        ingredient_endpoint,
        json=valid_ingredient_dict,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == valid_ingredient_dict
    mock_create_ingredient.assert_called_once_with(
        db=ANY,
        ingredient=ingredient_schema,
    )


@pytest.mark.asyncio
async def test_post_create_ingredient_raises_400(
    mock_create_ingredient: Mock,
    client: AsyncClient,
    ingredient_endpoint: str,
    valid_ingredient_dict: dict[str, Any],
    ingredient_schema: IngredientSchema,
) -> None:
    mock_create_ingredient.side_effect = DBIngredientCreationFailed(
        Exception('Error creating ingredient')
    )

    response = await client.post(
        ingredient_endpoint,
        json=valid_ingredient_dict,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': ['Error creating ingredient']}
    mock_create_ingredient.assert_called_once_with(
        db=ANY,
        ingredient=ingredient_schema,
    )


@pytest.mark.asyncio
async def test_get_ingredient_by_uuid(
    mock_get_ingredient: Mock,
    client: AsyncClient,
    ingredient_endpoint: str,
    valid_ingredient_dict: dict[str, Any],
    ingredient_schema: IngredientSchema,
) -> None:
    response = await client.get(f'{ingredient_endpoint}{uuid4()}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == valid_ingredient_dict


@pytest.mark.asyncio
async def test_put_update_ingredient(
    mock_update_ingredient: Mock,
    client: AsyncClient,
    ingredient_endpoint: str,
    valid_ingredient_dict: dict[str, Any],
    ingredient_schema: IngredientSchema,
) -> None:
    uuid = ingredient_schema.uuid

    response = await client.put(
        f'{ingredient_endpoint}{uuid}',
        json=valid_ingredient_dict,
    )

    mock_update_ingredient.assert_called_once_with(
        db=None,
        uuid=ingredient_schema.uuid,
        ingredient=ingredient_schema,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == valid_ingredient_dict


@pytest.mark.asyncio
async def test_put_update_ingredient_raises_400(
    mock_update_ingredient: Mock,
    client: AsyncClient,
    ingredient_endpoint: str,
    valid_ingredient_dict: dict[str, Any],
    ingredient_schema: IngredientSchema,
) -> None:
    mock_update_ingredient.side_effect = DBIngredientCreationFailed(
        ValueError('Invalid data')
    )

    response = await client.put(
        f'{ingredient_endpoint}{ingredient_schema.uuid}',
        json=valid_ingredient_dict,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': ['Invalid data']}
    mock_update_ingredient.assert_called_once_with(
        db=None,
        uuid=ingredient_schema.uuid,
        ingredient=ingredient_schema,
    )
