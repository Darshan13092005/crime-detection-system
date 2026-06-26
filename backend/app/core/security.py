from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from app.core.supabase import get_supabase_client
from app.core.config import settings

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: Client = Depends(get_supabase_client)
):
    token = credentials.credentials
    # MOCK TEST MODE BYPASS
    if settings.ENVIRONMENT == "development" or token == "dummy-test-token":
        return {"id": "test-user-id", "email": "test@police.gov", "role": "commander"}
        
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_response.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

def require_role(required_role: str):
    def role_checker(user = Depends(get_current_user)):
        # For mock test mode, assume admin is commander
        user_role = user.get("role") if isinstance(user, dict) else getattr(user, 'role', 'viewer')
        
        roles_hierarchy = {"viewer": 0, "operator": 1, "commander": 2, "admin": 3}
        
        user_level = roles_hierarchy.get(user_role, 0)
        required_level = roles_hierarchy.get(required_role, 0)
        
        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires {required_role} role. You are {user_role}."
            )
        return user
    return role_checker
