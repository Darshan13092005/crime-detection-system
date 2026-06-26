from supabase import Client
from app.schemas.alert import AlertCreate, AlertUpdate

class AlertService:
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table = "alerts"

    def get_alerts(self, limit: int = 100):
        res = self.supabase.table(self.table).select("*").order("created_at", desc=True).limit(limit).execute()
        return res.data

    def get_alert(self, alert_id: str):
        res = self.supabase.table(self.table).select("*").eq("id", alert_id).execute()
        if res.data:
            return res.data[0]
        return None

    def create_alert(self, alert: AlertCreate):
        res = self.supabase.table(self.table).insert(alert.model_dump()).execute()
        if res.data:
            return res.data[0]
        return None

    def update_alert(self, alert_id: str, alert: AlertUpdate):
        update_data = alert.model_dump(exclude_unset=True)
        res = self.supabase.table(self.table).update(update_data).eq("id", alert_id).execute()
        if res.data:
            return res.data[0]
        return None
