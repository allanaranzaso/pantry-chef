from typing import List
from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey, String, Table, Text, func
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pantry_chef.base_model import Base, BaseStatus, BaseTelemetry
from pantry_chef.ingredient.model import Ingredient
from pantry_chef.instruction.model import Instruction

ingredient_recipe_association = Table(
    'ingredient_recipe_association',
    Base.metadata,
    Column('recipe_uuid', SA_UUID(as_uuid=True), ForeignKey('recipe.uuid')),
    Column('ingredient_uuid', SA_UUID(as_uuid=True), ForeignKey('ingredient.uuid')),
)


class Recipe(Base, BaseStatus, BaseTelemetry):
    __tablename__ = 'recipe'

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    ingredients: Mapped[List[Ingredient]] = relationship(
        'Ingredient',
        secondary=ingredient_recipe_association,
        lazy='joined',
    )
    instructions: Mapped[List[Instruction]] = relationship(
        'Instruction',
        back_populates='recipe',
        lazy='joined',
        cascade='all, delete-orphan',
    )
    cuisine_type: Mapped[str] = mapped_column(String, nullable=False)
