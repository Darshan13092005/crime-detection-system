from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    camera_id: str
    alert_type: str  # e.g., 'weapon_detected', 'violence', 'criminal_spotted'
    severity: str    # e.g., 'low', 'medium', 'high', 'critical'
    description: Optional[str] = None
    snapshot_url: Optional[str] = None

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    status: Optional[str] = None  # e.g., 'new', 'acknowledged', 'resolved'
    resolution_notes: Optional[str] = None

class AlertResponse(AlertBase):
    id: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
