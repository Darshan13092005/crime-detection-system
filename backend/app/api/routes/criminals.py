from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.criminal import CriminalCreate, CriminalUpdate, CriminalResponse
from app.services.criminal_service import CriminalService
from app.api.dependencies import get_criminal_service
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CriminalResponse])
def get_criminals(
    criminal_service: CriminalService = Depends(get_criminal_service),
    user = Depends(get_current_user)
):
    return criminal_service.get_criminals()

@router.post("/", response_model=CriminalResponse, status_code=status.HTTP_201_CREATED)
def create_criminal(
    criminal: CriminalCreate,
    criminal_service: CriminalService = Depends(get_criminal_service),
    user = Depends(get_current_user)
):
    res = criminal_service.create_criminal(criminal)
    if not res:
        raise HTTPException(status_code=400, detail="Failed to create criminal")
    return res

@router.get("/{criminal_id}", response_model=CriminalResponse)
def get_criminal(
    criminal_id: str,
    criminal_service: CriminalService = Depends(get_criminal_service),
    user = Depends(get_current_user)
):
    criminal = criminal_service.get_criminal(criminal_id)
    if not criminal:
        raise HTTPException(status_code=404, detail="Criminal not found")
    return criminal

@router.put("/{criminal_id}", response_model=CriminalResponse)
def update_criminal(
    criminal_id: str,
    criminal: CriminalUpdate,
    criminal_service: CriminalService = Depends(get_criminal_service),
    user = Depends(get_current_user)
):
    res = criminal_service.update_criminal(criminal_id, criminal)
    if not res:
        raise HTTPException(status_code=404, detail="Criminal not found or update failed")
    return res
