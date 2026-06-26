from supabase import Client
from app.schemas.camera import CameraCreate, CameraUpdate

class CameraService:
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table = "cameras"

    def get_cameras(self):
        res = self.supabase.table(self.table).select("*").execute()
        return res.data

    def get_camera(self, camera_id: str):
        res = self.supabase.table(self.table).select("*").eq("id", camera_id).execute()
        if res.data:
            return res.data[0]
        return None

    def create_camera(self, camera: CameraCreate):
        res = self.supabase.table(self.table).insert(camera.model_dump()).execute()
        if res.data:
            return res.data[0]
        return None

    def update_camera(self, camera_id: str, camera: CameraUpdate):
        update_data = camera.model_dump(exclude_unset=True)
        res = self.supabase.table(self.table).update(update_data).eq("id", camera_id).execute()
        if res.data:
            return res.data[0]
        return None

    def delete_camera(self, camera_id: str):
        res = self.supabase.table(self.table).delete().eq("id", camera_id).execute()
        return res.data
