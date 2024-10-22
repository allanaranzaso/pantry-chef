from typing import List
from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlalchemy import func, String, ForeignKey, Number, Table, Index, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pantry_chef.base_model import Base, BaseStatus, BaseTelemetry
from pantry_chef.recipe.model import Recipe

recipe_ingredient_association = Table(
    'recipe_ingredient_association',
    Base.metadata,
    Column(
        'recipe_uuid',
        SA_UUID(as_uuid=True),
        ForeignKey('recipe.uuid'),
        nullable=False,
    ),
    Column(
        'ingredient_uuid',
        SA_UUID(as_uuid=True),
        ForeignKey('ingredient.uuid'),
        nullable=False,
    ),
    Index(
        'index_recipe_ingredient_association',
        'recipe_uuid',
        'ingredient_uuid',
        unique=True,
    ),
)


class Ingredient(Base, BaseStatus, BaseTelemetry):
    __tablename__ = 'ingredient'

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[float] = mapped_column(Number, nullable=False)
    uom: Mapped[str] = mapped_column(String, nullable=False)
    recipes: Mapped[List[Recipe]] = relationship(
        'Recipe',
        secondary=recipe_ingredient_association,
        lazy='joined',
    )
