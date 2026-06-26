from fastapi import APIRouter
from app.api.routes import cameras, auth, alerts, criminals, health, analytics, events, stream
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(cameras.router, prefix="/cameras", tags=["Cameras"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
api_router.include_router(criminals.router, prefix="/criminals", tags=["Criminals"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])
api_router.include_router(stream.router, prefix="/stream", tags=["Stream"])
