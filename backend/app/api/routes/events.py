from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.event import EventCreate, EventResponse
from app.services.event_service import EventService
from app.api.dependencies import get_event_service
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[EventResponse])
def get_events(
    limit: int = 100,
    event_service: EventService = Depends(get_event_service),
    user = Depends(get_current_user)
):
    return event_service.get_events(limit)

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event: EventCreate,
    event_service: EventService = Depends(get_event_service),
    # Might not require current_user if called by AI inference worker
):
    res = event_service.create_event(event)
    if not res:
        raise HTTPException(status_code=400, detail="Failed to create event")
    return res
