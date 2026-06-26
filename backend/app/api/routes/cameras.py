from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.camera import CameraCreate, CameraUpdate, CameraResponse
from app.services.camera_service import CameraService
from app.api.dependencies import get_camera_service
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CameraResponse])
def get_cameras(
    camera_service: CameraService = Depends(get_camera_service),
    user = Depends(get_current_user)
):
    return camera_service.get_cameras()

@router.post("/", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
def create_camera(
    camera: CameraCreate,
    camera_service: CameraService = Depends(get_camera_service),
    user = Depends(get_current_user)
):
    res = camera_service.create_camera(camera)
    if not res:
        raise HTTPException(status_code=400, detail="Failed to create camera")
    return res

@router.get("/{camera_id}", response_model=CameraResponse)
def get_camera(
    camera_id: str,
    camera_service: CameraService = Depends(get_camera_service),
    user = Depends(get_current_user)
):
    camera = camera_service.get_camera(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera

@router.put("/{camera_id}", response_model=CameraResponse)
def update_camera(
    camera_id: str,
    camera: CameraUpdate,
    camera_service: CameraService = Depends(get_camera_service),
    user = Depends(get_current_user)
):
    res = camera_service.update_camera(camera_id, camera)
    if not res:
        raise HTTPException(status_code=404, detail="Camera not found or update failed")
    return res

@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_camera(
    camera_id: str,
    camera_service: CameraService = Depends(get_camera_service),
    user = Depends(get_current_user)
):
    camera_service.delete_camera(camera_id)
    return None
