from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import UserLogin, UserRegister, Token
from app.services.auth_service import AuthService
from app.api.dependencies import get_auth_service
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    if settings.ENVIRONMENT == "development":
        # MOCK LOGIN
        return Token(access_token="dummy-test-token", token_type="bearer")
        
    res = auth_service.login(user_credentials.email, user_credentials.password)
    if not res:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return Token(access_token=res["access_token"], token_type="bearer")

@router.post("/register", response_model=dict)
def register(
    user_data: UserRegister,
    auth_service: AuthService = Depends(get_auth_service)
):
    res = auth_service.register(user_data.email, user_data.password)
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed")
    return {"message": "User registered successfully", "user": res}
