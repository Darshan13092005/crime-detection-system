from supabase import Client
from app.schemas.event import EventCreate

class EventService:
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table = "events"

    def get_events(self, limit: int = 100):
        res = self.supabase.table(self.table).select("*").order("created_at", desc=True).limit(limit).execute()
        return res.data

    def create_event(self, event: EventCreate):
        res = self.supabase.table(self.table).insert(event.model_dump()).execute()
        if res.data:
            return res.data[0]
        return None
