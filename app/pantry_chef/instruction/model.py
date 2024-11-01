from uuid import UUID, uuid4

from sqlalchemy import Column, Float, ForeignKey, Index, String, Table, Text, func
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column

from pantry_chef.base_model import Base, BaseStatus, BaseTelemetry

recipe_instruction_association = Table(
    'recipe_instruction_association',
    Base.metadata,
    Column(
        'recipe_uuid',
        SA_UUID(as_uuid=True),
        ForeignKey('recipe.uuid'),
        nullable=False,
    ),
    Column(
        'instruction_uuid',
        SA_UUID(as_uuid=True),
        ForeignKey('instruction.uuid'),
        nullable=False,
    ),
    Index(
        'index_recipe_instruction_association',
        'recipe_uuid',
        'instruction_uuid',
        unique=True,
    ),
)


class Instruction(Base, BaseStatus, BaseTelemetry):
    __tablename__ = 'instruction'

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid(),
    )
    step_number: Mapped[str] = mapped_column(
        String(2), server_default='1', nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text, server_default='There is no description available.', nullable=False
    )
    duration_ms: Mapped[int] = mapped_column(Float, nullable=False)
