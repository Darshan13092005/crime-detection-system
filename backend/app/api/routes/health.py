from fastapi import APIRouter
import time
import psutil
from app.core.supabase import get_supabase_client

router = APIRouter()

@router.get("/")
def get_health():
    # Basic system metrics
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    
    # DB check
    db_status = "offline"
    try:
        supabase = get_supabase_client()
        # A simple query to check DB connection
        res = supabase.table("cameras").select("id", count="exact").limit(1).execute()
        if res:
            db_status = "online"
    except Exception as e:
        db_status = f"error: {str(e)}"
        
    return {
        "status": "healthy" if db_status == "online" else "degraded",
        "timestamp": time.time(),
        "cpu_usage": cpu,
        "memory_usage": mem,
        "database": db_status
    }
