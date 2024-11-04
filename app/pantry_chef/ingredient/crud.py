from datetime import (
    UTC,
    datetime,
)
from uuid import (
    UUID,
    uuid4,
)

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from pantry_chef.ingredient.exceptions import (
    DBIngredientCreationFailed,
    IngredientNotFoundException,
)
from pantry_chef.ingredient.model import Ingredient
from pantry_chef.ingredient.schema import IngredientSchema


async def db_create_ingredient(
    db: AsyncSession, ingredient: IngredientSchema
) -> IngredientSchema:
    db_ingredient = Ingredient(
        **ingredient.model_dump(), created_at=datetime.now(tz=UTC), last_modify_by=uuid4()
    )
    try:
        IngredientSchema.model_validate(ingredient)
    except ValidationError as exc:
        raise DBIngredientCreationFailed(exc) from exc

    db.add(db_ingredient)
    try:
        await db.commit()
        await db.refresh(db_ingredient)
    except DBAPIError as exc:
        await db.rollback()
        raise DBIngredientCreationFailed(exc) from exc

    return ingredient


async def db_get_ingredient_by_uuid(
    db: AsyncSession,
    uuid: UUID,
) -> IngredientSchema:
    query = select(Ingredient).where(Ingredient.uuid == uuid)
    query_result = await db.execute(query)
    result = query_result.scalars().first()

    if not result:
        raise IngredientNotFoundException

    return IngredientSchema.model_validate(result)


async def db_update_ingredient(
    db: AsyncSession, uuid: UUID, ingredient: IngredientSchema
) -> IngredientSchema:
    db_ingredient = await db_get_ingredient_by_uuid(db, uuid)
    updated_fields = ingredient.model_dump(exclude_unset=True, exclude={'uuid'})

    for field, value in updated_fields.items():
        setattr(db_ingredient, field, value)

    try:
        await db.commit()

    except (IngredientNotFoundException, DBAPIError) as exc:
        await db.rollback()
        raise DBIngredientCreationFailed(exc) from exc

    await db.refresh(db_ingredient)
    return IngredientSchema.model_validate(db_ingredient)
