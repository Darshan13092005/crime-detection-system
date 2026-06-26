from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    camera_id: str
    event_type: str # 'person_detected', 'vehicle_detected'
    confidence: float
    bbox: Optional[str] = None # JSON string of bounding box

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
