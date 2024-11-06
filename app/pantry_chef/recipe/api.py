from uuid import UUID

from fastapi import (
    APIRouter,
    status,
)
from fastapi.responses import JSONResponse

from pantry_chef.dependencies import DBSession
from pantry_chef.recipe.crud import (
    db_create_recipe,
    db_get_recipe_by_uuid,
    db_update_recipe,
)
from pantry_chef.recipe.exceptions import (
    DBRecipeCreationFailed,
    RecipeNotFoundException,
)
from pantry_chef.recipe.schema import RecipeSchema

router = APIRouter(
    prefix='/recipe',
    tags=['recipe'],
)


@router.get(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=RecipeSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': dict[str, str],
            'description': 'The recipe was not found.',
        },
    },
)
async def get_recipe_by_uuid(
    db: DBSession,
    uuid: UUID,
) -> RecipeSchema | JSONResponse:
    try:
        return await db_get_recipe_by_uuid(db=db, uuid=uuid)
    except RecipeNotFoundException:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'detail': 'Recipe was not found.'},
        )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=RecipeSchema,
)
async def post_create_recipe(
    db: DBSession,
    recipe: RecipeSchema,
) -> RecipeSchema | JSONResponse:
    try:
        return await db_create_recipe(db=db, recipe=recipe)
    except DBRecipeCreationFailed as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': exc.detail},
        )


@router.put(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=RecipeSchema,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'model': dict[str, str],
            'description': 'The data failed integrity checks.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': dict[str, str],
            'description': 'The recipe was not found.',
        },
    },
)
async def put_update_recipe(
    db: DBSession,
    uuid: UUID,
    recipe: RecipeSchema,
) -> RecipeSchema | JSONResponse:
    try:
        return await db_update_recipe(db=db, uuid=uuid, recipe=recipe)
    except DBRecipeCreationFailed as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': exc.detail},
        )
    except RecipeNotFoundException:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'detail': 'Recipe was not found.'},
        )
