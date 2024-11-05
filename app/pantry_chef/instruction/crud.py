from datetime import (
    UTC,
    datetime,
)
from uuid import (
    UUID,
    uuid4,
)

from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql import select

from pantry_chef.dependencies import DBSession
from pantry_chef.instruction.exceptions import (
    DBInstructionCreationFailed,
    InstructionNotFoundException,
)
from pantry_chef.instruction.model import Instruction
from pantry_chef.instruction.schema import InstructionSchema


async def db_get_instruction_by_uuid(db: DBSession, uuid: UUID) -> InstructionSchema:
    query = select(Instruction).where(Instruction.uuid == uuid)
    result = await db.execute(query)
    instruction = result.scalars().first()

    if not instruction:
        raise InstructionNotFoundException

    return InstructionSchema.model_validate(instruction)


async def db_create_instruction(
    db: DBSession, instruction: InstructionSchema
) -> InstructionSchema:
    db_instruction = Instruction(
        **instruction.model_dump(),
        created_at=datetime.now(tz=UTC),
        last_modify_by=uuid4(),
    )

    db.add(db_instruction)

    try:
        await db.commit()
        await db.refresh(db_instruction)

    except DBAPIError as db_err:
        await db.rollback()
        raise DBInstructionCreationFailed(db_err) from db_err

    return instruction


async def db_update_instruction(
    db: DBSession, uuid: UUID, instruction: InstructionSchema
) -> InstructionSchema:
    db_instruction = await db_get_instruction_by_uuid(db=db, uuid=uuid)
    updated_fields = instruction.model_dump(exclude_unset=True, exclude={'uuid'})

    for field, value in updated_fields.items():
        setattr(db_instruction, field, value)

    try:
        await db.commit()

    except (InstructionNotFoundException, DBAPIError) as exc:
        await db.rollback()
        raise DBInstructionCreationFailed(exc) from exc

    await db.refresh(db_instruction)
    return InstructionSchema.model_validate(db_instruction)
