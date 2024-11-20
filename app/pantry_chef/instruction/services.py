from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from pantry_chef.instruction.crud import (
    db_create_instruction,
    db_get_instruction_by_uuid,
    db_update_instruction,
)
from pantry_chef.instruction.schema import InstructionSchema


async def create_instruction(
    db: AsyncSession,
    instruction: InstructionSchema,
) -> InstructionSchema:
    InstructionSchema.model_validate(instruction)
    db_instruction = await db_create_instruction(db=db, instruction=instruction)

    return InstructionSchema.model_validate(db_instruction)


async def get_instruction_by_uuid(
    db: AsyncSession,
    uuid: UUID,
) -> InstructionSchema:
    db_instruction = await db_get_instruction_by_uuid(db=db, uuid=uuid)

    return InstructionSchema.model_validate(db_instruction)


async def update_instruction(
    db: AsyncSession,
    uuid: UUID,
    instruction: InstructionSchema,
) -> InstructionSchema:
    db_instruction = await db_update_instruction(
        db=db, uuid=uuid, instruction=instruction
    )

    return await get_instruction_by_uuid(db=db, uuid=db_instruction.uuid)
