from uuid import UUID

from fastapi import (
    APIRouter,
    status,
)
from fastapi.responses import JSONResponse

from pantry_chef.common_exceptions import CustomValidationError
from pantry_chef.dependencies import DBSession
from pantry_chef.ingredient.crud import (
    db_create_ingredient,
    db_get_ingredient_by_uuid,
    db_update_ingredient,
)
from pantry_chef.ingredient.exceptions import (
    DBIngredientCreationFailed,
    IngredientNotFoundException,
)
from pantry_chef.ingredient.schema import IngredientSchema

router = APIRouter(
    prefix='/ingredient',
    tags=['ingredient'],
)


@router.get(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=IngredientSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': dict[str, str],
            'description': 'The ingredient was not found.',
        },
    },
)
async def get_ingredient_by_uuid(
    db: DBSession,
    uuid: UUID,
) -> IngredientSchema | JSONResponse:
    try:
        return await db_get_ingredient_by_uuid(db=db, uuid=uuid)
    except IngredientNotFoundException:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'detail': 'Ingredient was not found.'},
        )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=IngredientSchema,
)
async def post_create_ingredient(
    db: DBSession,
    ingredient: IngredientSchema,
) -> IngredientSchema | JSONResponse:
    try:
        return await db_create_ingredient(
            db=db,
            ingredient=ingredient,
        )
    except DBIngredientCreationFailed as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': exc.detail},
        )


@router.put(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=IngredientSchema,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'model': dict[str, str],
            'description': 'The data provided failed integrity checks.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': dict[str, str],
            'description': 'The ingredient was not found.',
        },
    },
)
async def put_update_ingredient(
    db: DBSession,
    uuid: UUID,
    ingredient: IngredientSchema,
) -> IngredientSchema | JSONResponse:
    try:
        return await db_update_ingredient(db=db, uuid=uuid, ingredient=ingredient)
    except (DBIngredientCreationFailed, CustomValidationError) as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': exc.detail},
        )
    except IngredientNotFoundException:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'detail': 'Ingredient was not found.'},
        )
