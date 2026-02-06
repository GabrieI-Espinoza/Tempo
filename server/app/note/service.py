from uuid import UUID
from typing import List, Optional
from fastapi import HTTPException, status
from app.tortoise.models.note import Note
from app.tortoise.models.event import Event
from app.tortoise.models.user import User
from app.note.schemas import NoteCreate, NoteUpdate


# Helper security function to verify event ownership and existence
async def validate_event(event_id: UUID, user: User) -> None:
    # Verify that the event with given ID exists and is owned by the user
    exists = await Event.filter(event_id=event_id, user=user).exists()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",  # Leak as little information as possible
        )


# Helper security function to verify note ownership and existence
async def validate_note(note_id: UUID, user: User) -> Note:
    # Verify that the note with given ID exists and is owned by the user
    note = await Note.get_or_none(note_id=note_id, user=user)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",  # Leak as little information as possible
        )
    # Once verified, return the note
    return note


# Function to create a new note
async def create_note(data: NoteCreate, user: User) -> Note:
    # If an event ID is provided, validate that the event exists and is owned by the user
    if data.event_id:
        await validate_event(data.event_id, user)

    return await Note.create(**data.model_dump(), user=user)


# Function to get user notes
async def get_notes(user: User, event_id: Optional[UUID] = None) -> List[Note]:
    query = Note.filter(user=user)
    # If an event ID is provided, filter notes by that event ID
    if event_id:
        query = query.filter(event_id=event_id)
    # Order notes by creation date and return the list of notes
    return await query.order_by("-created_at").all()


async def update_note(note_id: UUID, data: NoteUpdate, user: User) -> Note:
    # Validate that the note exists and is owned by the user
    note = await validate_note(note_id, user)

    # Extract only the fields that were provided in the update request
    update_data = data.model_dump(exclude_unset=True)
    new_event_id = update_data.get("event_id")

    # Drag and Drop Case
    if new_event_id:
        # Check if note is already linked to another event, and if so,
        # the user should not be allowed to change the link to a different event
        if note.event_id is not None and note.event_id != new_event_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Note is already linked to another event",
            )
        # If Orphan Note Case:
        # Validate that the new event exists and is owned by the user
        await validate_event(new_event_id, user)

    # Update the note with the provided fields and save changes to the database
    note.update_from_dict(update_data)
    await note.save()
    # Return the updated note
    return note


# Function to delete a note
async def delete_note(note_id: UUID, user: User) -> None:
    # Validate that the note exists and is owned by the user
    note = await validate_note(note_id, user)
    await note.delete()
