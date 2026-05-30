from uuid import UUID
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from app.categories.categories import CategoryLabel

MIN_EVENT_DURATION = timedelta(minutes=15)


def validate_15_min_increment(dt: datetime) -> datetime:
    if dt.minute % 15 != 0 or dt.second != 0 or dt.microsecond != 0:
        raise ValueError("Time must be on a 15-minute increment (e.g. 10:00, 10:15, 10:30, 10:45)")
    return dt


# Base schema for event, shares fields with children
class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    category: CategoryLabel = CategoryLabel.OTHER
    recurring: bool = False

    @field_validator("start_time", "end_time")
    @classmethod
    def check_increment(cls, value: datetime) -> datetime:
        return validate_15_min_increment(value)

    @model_validator(mode="after")
    def validate_time(self):
        if self.end_time - self.start_time < MIN_EVENT_DURATION:
            raise ValueError("Event must be at least 15 minutes long")
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
