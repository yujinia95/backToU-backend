from fastapi import APIRouter
from app.schemas.user import SignupRequest, SignupResponse
from app.services.auth_service import create_user

router = APIRouter(tags=["auth"])

@router.post("/signup")
def signup(requestedUser: SignupRequest) -> SignupResponse:
    return create_user(requestedUser)

