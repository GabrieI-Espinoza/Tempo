from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status

from app.tortoise.models.event import Event
from app.tortoise.models.user import User
from app.event.schemas import (
    EventCreate,
    EventUpdate,
    validate_event_times,
)


async def get_owned_event(event_id: UUID, user: User) -> Event:
    """Return an event only if it belongs to the user."""
    event = await Event.get_or_none(event_id=event_id, user=user)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return event


async def create_event(data: EventCreate, user: User) -> Event:
    """Create an event for the specified user."""
    return await Event.create(**data.model_dump(), user=user)


async def update_event(event_id: UUID, data: EventUpdate, user: User) -> Event:
    """Update an existing event for the specified user."""
    event = await get_owned_event(event_id, user)
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

    event.update_from_dict(update_data)
    await event.save()
    return event


async def get_user_events(user: User) -> list[Event]:
    """Return all events belonging to the specified user."""
    return await Event.filter(user=user).order_by("start_time").all()


async def get_user_events_between(
    user: User, start_time: datetime, end_time: datetime
) -> list[Event]:
    """Return all events belonging to the specified user that are between the specified start and end times."""
    return (
        await Event.filter(
            user=user, start_time__gte=start_time, end_time__lte=end_time
        )
        .order_by("start_time")
        .all()
    )


async def delete_user_event(event_id: UUID, user: User) -> None:
    """Delete an event belonging to the specified user."""
    event = await get_owned_event(event_id, user)
    await event.delete()
