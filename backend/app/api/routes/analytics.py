from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import datetime, timedelta
from app.core.security import get_current_user
from app.core.supabase import get_supabase_client

router = APIRouter()

@router.get("/")
def get_analytics(user = Depends(get_current_user)) -> Dict[str, Any]:
    # Mock data for demonstration since we can't easily perform complex aggregations 
    # directly via simple supabase-py calls without custom RPCs.
    
    # In a real scenario, this would aggregate from the `events` and `alerts` tables.
    return {
        "total_incidents_today": 12,
        "active_cameras": 4,
        "offline_cameras": 1,
        "recent_alerts": [
            {"time": "10:00", "count": 2},
            {"time": "11:00", "count": 5},
            {"time": "12:00", "count": 1},
            {"time": "13:00", "count": 4}
        ],
        "incidents_by_type": {
            "weapon_detected": 3,
            "fight_detected": 4,
            "suspicious_activity": 5
        },
        "incidents_by_camera": {
            "cam-01-front": 5,
            "cam-02-hall": 2,
            "cam-03-exit": 5
        }
    }
