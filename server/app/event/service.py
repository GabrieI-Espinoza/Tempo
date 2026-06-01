from uuid import UUID
from fastapi import HTTPException, status
from app.tortoise.models.event import Event
from app.tortoise.models.user import User
from app.event.schemas import (
    EventCreate,
    EventUpdate,
    validate_event_times,
)


# Helper to verify event ownership and existence
async def validate_event(event_id: UUID, user: User) -> Event:
    event = await Event.get_or_none(event_id=event_id, user=user)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return event


# Function to create a new event for a user
async def create_event(data: EventCreate, user: User) -> Event:
    return await Event.create(**data.model_dump(), user=user)


# Function to update an existing event for a user
async def update_event(event_id: UUID, data: EventUpdate, user: User) -> Event:
    event = await validate_event(event_id, user)

    # Retrieve only the fields that were provided in the update request
    update_data = data.model_dump(exclude_unset=True)

    new_start = update_data.get("start_time", event.start_time)
    new_end = update_data.get("end_time", event.end_time)

    try:
        validate_event_times(new_start, new_end)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    # Once validation is complete, update the event with the new data
    event.update_from_dict(update_data)

    # Ensure event is saved with the updated data in the database, and then return the updated event
    await event.save()
    return event


# Function to retrieve all events for a specific user
async def get_user_events(user: User) -> list[Event]:
    return await Event.filter(user=user).all()


# Function to delete an event for a user
async def delete_user_event(event_id: UUID, user: User) -> None:
    event = await validate_event(event_id, user)
    await event.delete()
