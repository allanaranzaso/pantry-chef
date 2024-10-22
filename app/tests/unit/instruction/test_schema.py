from uuid import UUID

import pytest

from pantry_chef.instruction.schema import InstructionSchema


def test_instruction_valid_schema(instruction_schema: InstructionSchema) -> None:
    valid_instruction_schema = instruction_schema.model_dump()

    assert InstructionSchema.model_validate(valid_instruction_schema)


@pytest.mark.parametrize(
    ('field', 'invalid_value'),
    [
        ('step_number', 1),
        ('description', ''),
        ('recipe_uuids', ['invalid value']),
        ('duration_ms', -1),
        ('duration_ms', 'Invalid value'),
    ],
)
def test_instruction_invalid_schema(
        field: str,
        invalid_value: str,
        instruction_schema: InstructionSchema
) -> None:
    invalid_instruction_schema = instruction_schema.model_dump()
    invalid_instruction_schema[field] = invalid_value
    error_msg = rf'1 validation error for.+\n{field}(\.0)?\n.+'

    with pytest.raises(ValueError, match=error_msg):
        InstructionSchema.model_validate(invalid_instruction_schema)


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('Thaw chicken', 'Thaw chicken'),
    ]
)
def test_instruction_schema_default_values(value: str, expected: str) -> None:
    instruction = InstructionSchema(description=value)

    assert isinstance(instruction.uuid, UUID)
    assert instruction.step_number == '1'
    assert instruction.description == expected
    assert instruction.recipe_uuids == []
    assert instruction.duration_ms == 0
