from typing import Any
from unittest.mock import (
    ANY,
    Mock,
)

import pytest
from fastapi import status
from httpx import AsyncClient

from pantry_chef.instruction.exceptions import (
    DBInstructionCreationFailed,
    InstructionNotFoundException,
)
from pantry_chef.instruction.schema import InstructionSchema


@pytest.fixture
def instruction_endpoint():
    return '/api/v1/instruction/'


@pytest.fixture
def mock_get_instruction(
    mocker: Mock,
    instruction_schema: InstructionSchema,
) -> Mock:
    mock = mocker.patch('pantry_chef.instruction.api.db_get_instruction_by_uuid')
    mock.return_value = instruction_schema

    return mock


@pytest.fixture
def mock_create_instruction(
    instruction_schema: InstructionSchema,
    mocker: Mock,
) -> Mock:
    mock = mocker.patch('pantry_chef.instruction.api.db_create_instruction')
    mock.return_value = instruction_schema

    return mock


@pytest.fixture
def mock_update_instruction(
    instruction_schema: InstructionSchema,
    mocker: Mock,
) -> Mock:
    mock = mocker.patch('pantry_chef.instruction.api.db_update_instruction')
    mock.return_value = instruction_schema

    return mock


@pytest.fixture
def valid_instruction_dict(
    instruction_schema: InstructionSchema,
) -> dict[str, Any]:
    return instruction_schema.model_dump(mode='json', by_alias=True)


@pytest.mark.asyncio
async def test_post_create_instruction(
    mock_create_instruction: Mock,
    client: AsyncClient,
    instruction_endpoint: str,
    valid_instruction_dict: dict[str, Any],
    instruction_schema: InstructionSchema,
):
    response = await client.post(
        instruction_endpoint,
        json=valid_instruction_dict,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == valid_instruction_dict
    mock_create_instruction.assert_called_once_with(
        db=ANY,
        instruction=instruction_schema,
    )


@pytest.mark.asyncio
async def test_post_create_instruction_raises_400(
    mock_create_instruction: Mock,
    client: AsyncClient,
    instruction_endpoint: str,
    valid_instruction_dict: dict[str, Any],
    instruction_schema: InstructionSchema,
):
    mock_create_instruction.side_effect = DBInstructionCreationFailed(
        Exception('Test exception'),
    )

    response = await client.post(
        instruction_endpoint,
        json=valid_instruction_dict,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': ['Test exception']}
    mock_create_instruction.assert_called_once_with(
        db=ANY,
        instruction=instruction_schema,
    )


@pytest.mark.asyncio
async def test_get_instruction_by_uuid(
    mock_get_instruction: Mock,
    client: AsyncClient,
    instruction_endpoint: str,
    valid_instruction_dict: dict[str, Any],
    instruction_schema: InstructionSchema,
):
    response = await client.get(f'{instruction_endpoint}{instruction_schema.uuid}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == valid_instruction_dict
    mock_get_instruction.assert_called_once_with(
        db=None,
        uuid=instruction_schema.uuid,
    )


@pytest.mark.asyncio
async def test_get_instruction_not_found(
    mock_get_instruction: Mock,
    client: AsyncClient,
    instruction_endpoint: str,
    instruction_schema: InstructionSchema,
):
    mock_get_instruction.side_effect = InstructionNotFoundException(
        'Instruction not found',
    )

    response = await client.get(f'{instruction_endpoint}{instruction_schema.uuid}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Instruction was not found.'}
    mock_get_instruction.assert_called_once_with(
        db=ANY,
        uuid=instruction_schema.uuid,
    )


@pytest.mark.asyncio
async def test_put_update_instruction(
    mock_update_instruction: Mock,
    client: AsyncClient,
    instruction_endpoint: str,
    valid_instruction_dict: dict[str, Any],
    instruction_schema: InstructionSchema,
):
    response = await client.put(
        f'{instruction_endpoint}{instruction_schema.uuid}',
        json=valid_instruction_dict,
    )

    mock_update_instruction.assert_called_once_with(
        db=None,
        uuid=instruction_schema.uuid,
        instruction=instruction_schema,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == valid_instruction_dict


@pytest.mark.asyncio
async def test_put_update_instruction_raises_400(
    mock_update_instruction: Mock,
    client: AsyncClient,
    instruction_endpoint: str,
    valid_instruction_dict: dict[str, Any],
    instruction_schema: InstructionSchema,
):
    mock_update_instruction.side_effect = DBInstructionCreationFailed(
        ValueError('Invalid data')
    )

    response = await client.put(
        f'{instruction_endpoint}{instruction_schema.uuid}',
        json=valid_instruction_dict,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': ['Invalid data']}
    mock_update_instruction.assert_called_once_with(
        db=None,
        uuid=instruction_schema.uuid,
        instruction=instruction_schema,
    )
