import os
import cv2
import uuid
import time
from typing import Optional, Dict
import numpy as np

from app.schemas.alert import AlertCreate
from app.schemas.event import EventCreate
from app.core.supabase import get_supabase_client
from app.services.notification_service import NotificationService

class EventDispatcher:
    def __init__(self, snapshot_dir: str = "data/snapshots"):
        self.snapshot_dir = snapshot_dir
        os.makedirs(self.snapshot_dir, exist_ok=True)
        self.supabase = get_supabase_client()
        # To prevent spamming, store last alert times per camera and type
        self.last_alerts: Dict[str, float] = {}
        self.cooldown_seconds = 30 # Wait 30s before sending another alert of same type

    def save_snapshot(self, frame, event_type: str) -> str:
        """Saves a frame locally and returns the path/url"""
        timestamp = int(time.time())
        unique_id = uuid.uuid4().hex[:8]
        filename = f"{event_type}_{timestamp}_{unique_id}.jpg"
        filepath = os.path.join(self.snapshot_dir, filename)
        
        cv2.imwrite(filepath, frame)
        return filepath # In production, you might upload to Supabase Storage here and return URL.

    def dispatch_alert(self, camera_id: str, alert_type: str, severity: str, description: str, frame=None):
        alert_key = f"{camera_id}_{alert_type}"
        current_time = time.time()
        
        if alert_key in self.last_alerts:
            if current_time - self.last_alerts[alert_key] < self.cooldown_seconds:
                return False # Cooldown active

        self.last_alerts[alert_key] = current_time

        snapshot_url = None
        if frame is not None:
            snapshot_url = self.save_snapshot(frame, alert_type)

        alert_data = AlertCreate(
            camera_id=camera_id,
            alert_type=alert_type,
            severity=severity,
            description=description,
            snapshot_url=snapshot_url
        )
        
        # Directly insert to DB via service/client
        try:
            res = self.supabase.table("alerts").insert(alert_data.model_dump()).execute()
            print(f"[ALERT DISPATCHED] {alert_type.upper()} on camera {camera_id}. DB Res: {res.data}")
            
            # Fire notifications (Email/Telegram) asynchronously
            NotificationService.dispatch_alert(alert_type, severity, camera_id, description)
            return True
        except Exception as e:
            print(f"Failed to dispatch alert to database: {e}")
            return False

    def dispatch_event(self, camera_id: str, event_type: str, confidence: float, bbox: str = None):
        event_data = EventCreate(
            camera_id=camera_id,
            event_type=event_type,
            confidence=confidence,
            bbox=bbox
        )
        self.supabase.table("events").insert(event_data.model_dump()).execute()
        print(f"[EVENT LOGGED] {event_type} on camera {camera_id}")
