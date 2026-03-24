from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# Base schema for note, shares fields with children
class NoteBase(BaseModel):
    content: str = Field(..., min_length=1)


# Schema for creating a note, inherits all fields from parent
class NoteCreate(NoteBase):
    event_id: Optional[UUID] = None


# Schema for updating a note, keeps all fields optional to allow partial updates
class NoteUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)
    event_id: Optional[UUID] = None


# Schema for note response
class NoteResponse(NoteBase):
    note_id: UUID
    event_id: Optional[UUID] = None
    created_at: datetime

    # Allows this response schema to be created directly from a Note model instance
    model_config = ConfigDict(from_attributes=True)
