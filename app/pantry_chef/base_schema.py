from datetime import datetime, timezone
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class StatusEnum(str, Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    DEPRECATED = 'DEPRECATED'


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class BaseTelemetrySchema(BaseModel):
    _published_by: UUID | None = None
    _published_at: datetime | None = None
    _last_modify_at: datetime = datetime.now(tz=timezone.utc)
    _last_modify_by: UUID | None = None
    _created_by: UUID | None = None
    _created_at: datetime = datetime.now(tz=timezone.utc)


class BaseStatusSchema(BaseModel):
    status: StatusEnum = StatusEnum.DRAFT
