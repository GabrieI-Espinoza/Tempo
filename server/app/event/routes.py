from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.auth.dependencies import get_current_user
from app.tortoise.models.user import User
from app.event.schemas import EventCreate, EventUpdate, EventResponse
from app.event.service import (
    create_event,
    update_event,
    get_user_events,
    delete_user_event,
)

# APIRouter for event routes
router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_new_event(
    data: EventCreate, current_user: User = Depends(get_current_user)
):
    return await create_event(data, current_user)


@router.get("/", response_model=List[EventResponse])
async def list_user_events(current_user: User = Depends(get_current_user)):
    return await get_user_events(current_user)


@router.patch("/{event_id}", response_model=EventResponse)
async def patch_event(
    event_id: UUID, data: EventUpdate, current_user: User = Depends(get_current_user)
):
    return await update_event(event_id, data, current_user)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: UUID, current_user: User = Depends(get_current_user)):
    await delete_user_event(event_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
