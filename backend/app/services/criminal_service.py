from supabase import Client
from app.schemas.criminal import CriminalCreate, CriminalUpdate

class CriminalService:
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table = "criminals"

    def get_criminals(self):
        res = self.supabase.table(self.table).select("*").execute()
        return res.data

    def get_criminal(self, criminal_id: str):
        res = self.supabase.table(self.table).select("*").eq("id", criminal_id).execute()
        if res.data:
            return res.data[0]
        return None

    def create_criminal(self, criminal: CriminalCreate):
        res = self.supabase.table(self.table).insert(criminal.model_dump()).execute()
        if res.data:
            return res.data[0]
        return None

    def update_criminal(self, criminal_id: str, criminal: CriminalUpdate):
        update_data = criminal.model_dump(exclude_unset=True)
        res = self.supabase.table(self.table).update(update_data).eq("id", criminal_id).execute()
        if res.data:
            return res.data[0]
        return None
