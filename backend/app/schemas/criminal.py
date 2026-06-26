from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CriminalBase(BaseModel):
    first_name: str
    last_name: str
    alias: Optional[str] = None
    known_crimes: Optional[str] = None
    threat_level: str = "medium" # 'low', 'medium', 'high'
    status: str = "wanted" # 'wanted', 'captured'

class CriminalCreate(CriminalBase):
    face_encoding: Optional[List[float]] = None
    image_url: Optional[str] = None

class CriminalUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    alias: Optional[str] = None
    known_crimes: Optional[str] = None
    threat_level: Optional[str] = None
    status: Optional[str] = None
    face_encoding: Optional[List[float]] = None
    image_url: Optional[str] = None

class CriminalResponse(CriminalBase):
    id: str
    image_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
