from uuid import UUID

from fastapi import (
    APIRouter,
    status,
)
from fastapi.responses import JSONResponse

from pantry_chef.dependencies import DBSession
from pantry_chef.instruction.crud import (
    db_create_instruction,
    db_get_instruction_by_uuid,
    db_update_instruction,
)
from pantry_chef.instruction.exceptions import (
    DBInstructionCreationFailed,
    InstructionNotFoundException,
)
from pantry_chef.instruction.schema import InstructionSchema

router = APIRouter(
    prefix='/instruction',
    tags=['instruction'],
)


@router.get(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=InstructionSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': dict[str, str],
            'description': 'The instruction was not found.',
        },
    },
)
async def get_instruction_by_uuid(
    db: DBSession,
    uuid: UUID,
) -> InstructionSchema | JSONResponse:
    try:
        return await db_get_instruction_by_uuid(db=db, uuid=uuid)
    except InstructionNotFoundException:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'detail': 'Instruction was not found.'},
        )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=InstructionSchema,
)
async def post_create_instruction(
    db: DBSession,
    instruction: InstructionSchema,
) -> InstructionSchema | JSONResponse:
    try:
        return await db_create_instruction(db=db, instruction=instruction)
    except DBInstructionCreationFailed as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': exc.detail},
        )


@router.put(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=InstructionSchema,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'model': dict[str, str],
            'description': 'The data provided failed integrity checks.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': dict[str, str],
            'description': 'The instruction was not found.',
        },
    },
)
async def put_update_instruction(
    db: DBSession,
    uuid: UUID,
    instruction: InstructionSchema,
) -> InstructionSchema | JSONResponse:
    try:
        return await db_update_instruction(db=db, uuid=uuid, instruction=instruction)
    except DBInstructionCreationFailed as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': exc.detail},
        )
    except InstructionNotFoundException:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'detail': 'Instruction was not found.'},
        )
