from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel


class PlanRead(SQLModel):
    id: UUID
    group_version_id: UUID
    name: str
    content: str
    bookmark: bool
    created_at: datetime
    user_id: UUID


class PlanCreate(SQLModel):
    name: str
    content: str
