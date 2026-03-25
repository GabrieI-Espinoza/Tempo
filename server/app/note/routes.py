from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, status, Response
from app.auth.dependencies import get_current_user
from app.tortoise.models.user import User
from app.note.schemas import NoteCreate, NoteUpdate, NoteResponse
from app.note.service import create_note, get_notes, update_note, delete_note

# APIRouter for note routes
router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_new_note(
    data: NoteCreate, current_user: User = Depends(get_current_user)
):
    return await create_note(data, current_user)


@router.get("/", response_model=List[NoteResponse])
async def list_notes(
    event_id: Optional[UUID] = None, current_user: User = Depends(get_current_user)
):
    # Handles both cases:
    # 1. All notes case: GET /notes
    # 2. Notes for a specific event case: GET /notes?event_id=...
    return await get_notes(current_user, event_id)


@router.patch("/{note_id}", response_model=NoteResponse)
async def patch_note(
    note_id: UUID, data: NoteUpdate, current_user: User = Depends(get_current_user)
):
    return await update_note(note_id, data, current_user)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_note(note_id: UUID, current_user: User = Depends(get_current_user)):
    await delete_note(note_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
