import datetime
import uuid
from typing import Any

import sqlalchemy as sa
from sqlalchemy import JSON, TIMESTAMP, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON,
        datetime.datetime: TIMESTAMP(timezone=True),
    }


class BaseTelemetry:
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now,
        server_default=sa.func.current_timestamp(),
        nullable=False,
    )
    last_updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        server_default=sa.func.current_timestamp(),
        nullable=False,
    )
    last_modify_by: Mapped[uuid.UUID] = mapped_column(nullable=False)


StructureStatus = ['draft', 'published', 'archived']


class BaseStatus:
    status: Mapped[StructureStatus] = mapped_column(
        String(10),
        default='draft',
        server_default='draft',
    )
