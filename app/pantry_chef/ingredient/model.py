from uuid import UUID, uuid4

from sqlalchemy import Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from pantry_chef.base_model import Base, BaseStatus, BaseTelemetry


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
