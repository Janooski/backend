import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class Plan(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    group_version_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(nullable=False)
    content: str
    bookmark: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: uuid.UUID = Field(nullable=False, foreign_key="user.id")
