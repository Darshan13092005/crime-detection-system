from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.alert import AlertCreate, AlertUpdate, AlertResponse
from app.services.alert_service import AlertService
from app.api.dependencies import get_alert_service
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
def get_alerts(
    limit: int = 100,
    alert_service: AlertService = Depends(get_alert_service),
    user = Depends(get_current_user)
):
    return alert_service.get_alerts(limit)

@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert: AlertCreate,
    alert_service: AlertService = Depends(get_alert_service),
    # Might not require current_user if called by AI inference worker
):
    res = alert_service.create_alert(alert)
    if not res:
        raise HTTPException(status_code=400, detail="Failed to create alert")
    return res

@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: str,
    alert: AlertUpdate,
    alert_service: AlertService = Depends(get_alert_service),
    user = Depends(get_current_user)
):
    res = alert_service.update_alert(alert_id, alert)
    if not res:
        raise HTTPException(status_code=404, detail="Alert not found or update failed")
    return res
