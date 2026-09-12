from fastapi import APIRouter, HTTPException
from app.schemas.user import SignupRequest, SignupResponse, LoginRequest
from app.services.auth_service import create_user, login_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/signup")
def signup(requestedUser: SignupRequest) -> SignupResponse:
    return create_user(requestedUser)

@router.post("/login")
def login(data: LoginRequest) -> SignupResponse:
    try: 
        return login_user(data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
