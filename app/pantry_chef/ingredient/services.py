from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from pantry_chef.ingredient.crud import (
    db_create_ingredient,
    db_get_ingredient_by_uuid,
    db_update_ingredient,
)
from pantry_chef.ingredient.schema import IngredientSchema


async def get_ingredient_by_uuid(
    db: AsyncSession,
    uuid: UUID,
) -> IngredientSchema:
    db_ingredient = await db_get_ingredient_by_uuid(db=db, uuid=uuid)

    return IngredientSchema.model_validate(db_ingredient)


async def create_ingredient(
    db: AsyncSession,
    ingredient: IngredientSchema,
) -> IngredientSchema:
    db_ingredient = await db_create_ingredient(db=db, ingredient=ingredient)

    return IngredientSchema.model_validate(db_ingredient)


async def update_ingredient(
    db: AsyncSession,
    uuid: UUID,
    ingredient: IngredientSchema,
) -> IngredientSchema:
    db_ingredient = await db_update_ingredient(db=db, uuid=uuid, ingredient=ingredient)

    return await get_ingredient_by_uuid(db=db, uuid=db_ingredient.uuid)
