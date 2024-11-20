from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey, String, Table, Text, func
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pantry_chef.base_model import Base, BaseStatus, BaseTelemetry
from pantry_chef.ingredient.model import Ingredient
from pantry_chef.instruction.model import Instruction

recipe_instruction_association = Table(
    'recipe_instruction_association',
    Base.metadata,
    Column(
        'recipe_uuid',
        SA_UUID(as_uuid=True),
        ForeignKey('recipe.uuid'),
    ),
    Column(
        'instruction_uuid',
        SA_UUID(as_uuid=True),
        ForeignKey('instruction.uuid'),
    ),
)

recipe_ingredient_association = Table(
    'recipe_ingredient_association',
    Base.metadata,
    Column(
        'recipe_uuid',
        SA_UUID(as_uuid=True),
        ForeignKey('recipe.uuid'),
    ),
    Column(
        'ingredient_uuid',
        SA_UUID(as_uuid=True),
        ForeignKey('ingredient.uuid'),
    ),
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
    ingredients: Mapped[list[Ingredient]] = relationship(
        'Ingredient',
        secondary=recipe_ingredient_association,
    )
    instructions: Mapped[list[Instruction]] = relationship(
        'Instruction',
        secondary=recipe_instruction_association,
        lazy='joined',
    )

    cuisine_type: Mapped[str] = mapped_column(String, nullable=False)
