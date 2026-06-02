from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    content: str = Field(min_length=1)


class NoteCreate(NoteBase):
    """Request body for creating a new note, can be optionally linked to an event."""

    event_id: Optional[UUID] = None
    model_config = ConfigDict(extra="forbid")


class NoteUpdate(BaseModel):
    """Request body for updateing an existing note."""

    content: Optional[str] = Field(None, min_length=1)
    event_id: Optional[UUID] = None

    model_config = ConfigDict(extra="forbid")


class NoteResponse(NoteBase):
    note_id: UUID
    event_id: Optional[UUID] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
