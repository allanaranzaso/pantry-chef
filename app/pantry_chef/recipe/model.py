import datetime
from typing import Dict, Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import func, String, Text, JSON
from sqlalchemy.orm import mapped_column, Mapped

from app.pantry_chef.base_model import Base, BaseStatus


class Recipe(Base, BaseStatus):
    __tablename__ = 'recipe'

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    ingredients: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    instructions: Mapped[Dict[int, str]] = mapped_column(JSON, nullable=False)
    cuisine_type: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    last_updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now,
        nullable=False,
        onupdate=datetime.datetime.now,
        server_default=sa.func.current_timestamp(),
    )
