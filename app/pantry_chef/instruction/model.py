from uuid import UUID, uuid4

from sqlalchemy import Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from pantry_chef.base_model import Base, BaseStatus, BaseTelemetry


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
