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
from pantry_chef.recipe.exceptions import (
    DBRecipeCreationFailed,
    RecipeNotFoundException,
)
from pantry_chef.recipe.model import Recipe
from pantry_chef.recipe.schema import RecipeSchema


async def db_get_recipe_by_uuid(
    db: DBSession,
    uuid: UUID,
) -> RecipeSchema:
    query = select(Recipe).where(Recipe.uuid == uuid)
    result = await db.execute(query)

    recipe = result.scalars().first()
    if not recipe:
        raise RecipeNotFoundException

    return RecipeSchema.model_validate(recipe)


async def db_create_recipe(
    db: DBSession,
    recipe: RecipeSchema,
) -> RecipeSchema:
    db_recipe = Recipe(
        **recipe.model_dump(),
        created_at=datetime.now(tz=UTC),
        last_modify_by=uuid4(),
    )

    db.add(db_recipe)

    try:
        await db.commit()
        await db.refresh(db_recipe)

    except DBAPIError as db_err:
        await db.rollback()
        raise DBRecipeCreationFailed(db_err) from db_err

    return recipe


async def db_update_recipe(
    db: DBSession,
    uuid: UUID,
    recipe: RecipeSchema,
) -> RecipeSchema:
    db_recipe = await db_get_recipe_by_uuid(db=db, uuid=uuid)
    updated_fields = recipe.model_dump(exclude_unset=True, exclude={'uuid'})

    for field, value in updated_fields.items():
        setattr(db_recipe, field, value)

    try:
        await db.commit()

    except (RecipeNotFoundException, DBAPIError) as exc:
        await db.rollback()
        raise DBRecipeCreationFailed(exc) from exc

    await db.refresh(db_recipe)
    return RecipeSchema.model_validate(db_recipe)
