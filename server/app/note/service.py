from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status

from app.note.schemas import NoteCreate, NoteUpdate
from app.tortoise.models.event import Event
from app.tortoise.models.note import Note
from app.tortoise.models.user import User


async def ensure_owned_event(event_id: UUID, user: User) -> None:
    """Raise 404 unless the event exists and is owned by the user."""
    exists = await Event.filter(event_id=event_id, user=user).exists()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )


async def get_owned_note(note_id: UUID, user: User) -> Note:
    """Return the note if it exists and is owned by the user."""
    note = await Note.get_or_none(note_id=note_id, user=user)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    return note


async def create_note(data: NoteCreate, user: User) -> Note:
    """Create a new note for the user."""
    if data.event_id is not None:
        await ensure_owned_event(data.event_id, user)

    return await Note.create(**data.model_dump(), user=user)


async def get_notes(user: User, event_id: Optional[UUID] = None) -> list[Note]:
    """Return a list of notes for the user, optionally filtered by event."""
    query = Note.filter(user=user)
    if event_id is not None:
        query = query.filter(event_id=event_id)
    return await query.order_by("-created_at").all()


async def update_note(note_id: UUID, data: NoteUpdate, user: User) -> Note:
    """Update an existing note while ensuring ownership and valid event linkage."""
    note = await get_owned_note(note_id, user)
    update_data = data.model_dump(exclude_unset=True)

    new_event_id = update_data.get("event_id")

    if new_event_id is not None:
        if note.event_id is not None and note.event_id != new_event_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Note is already linked to another event",
            )

        await ensure_owned_event(new_event_id, user)

    note.update_from_dict(update_data)
    await note.save()
    return note


async def delete_note(note_id: UUID, user: User) -> None:
    """Delete a note if it exists and is owned by the user."""
    note = await get_owned_note(note_id, user)
    await note.delete()
