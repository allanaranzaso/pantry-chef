from uuid import UUID, uuid4

from sqlalchemy import Column, Float, ForeignKey, Index, String, Table, func
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column

from pantry_chef.base_model import Base, BaseStatus, BaseTelemetry

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
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    uom: Mapped[str] = mapped_column(String, nullable=False)
