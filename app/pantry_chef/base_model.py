import datetime
from typing import Any

from sqlalchemy import JSON, TIMESTAMP, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON,
        datetime.datetime: TIMESTAMP(timezone=True),
    }


StructureStatus = ['draft', 'published', 'archived']


class BaseStatus:
    status: Mapped[StructureStatus] = mapped_column(
        String(20),
        default='draft',
        server_default='draft',
    )
