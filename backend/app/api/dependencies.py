from fastapi import Depends
from supabase import Client
from app.core.supabase import get_supabase_client
from app.services.auth_service import AuthService
from app.services.camera_service import CameraService
from app.services.alert_service import AlertService
from app.services.criminal_service import CriminalService
from app.services.event_service import EventService

def get_auth_service(supabase: Client = Depends(get_supabase_client)) -> AuthService:
    return AuthService(supabase)

def get_camera_service(supabase: Client = Depends(get_supabase_client)) -> CameraService:
    return CameraService(supabase)

def get_alert_service(supabase: Client = Depends(get_supabase_client)) -> AlertService:
    return AlertService(supabase)

def get_criminal_service(supabase: Client = Depends(get_supabase_client)) -> CriminalService:
    return CriminalService(supabase)

def get_event_service(supabase: Client = Depends(get_supabase_client)) -> EventService:
    return EventService(supabase)
