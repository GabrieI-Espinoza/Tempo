from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.categories.categories import CategoryLabel


# Base schema for event, shares fields with children
class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    category: CategoryLabel = CategoryLabel.OTHER
    recurring: bool = False

    @model_validator(mode="after")
    def validate_time(self):
        # Enaures that the end time is after the start time
        if self.end_time < self.start_time:
            raise ValueError("end time must be after start time")
        return self


# Schema for creating an event, inherits all fields from parent
class EventCreate(EventBase):
    pass


# Schema for updating an event, keeps all fields optional to allow partial updates
class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    category: Optional[CategoryLabel] = None
    recurring: Optional[bool] = None


# Schema for event response
class EventResponse(EventBase):
    event_id: UUID

    # Allows this response schema to be created directly from an Event model instance
    model_config = ConfigDict(from_attributes=True)
