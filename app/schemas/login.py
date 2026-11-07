"""Schema for user login."""

from pydantic import BaseModel, EmailStr, Field
from app.schemas.user import UserResponse
from app.core.constants import (
    EMAIL_MAX_LENGTH,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
)


class UserLogin(BaseModel):
    """Validate the email and password received in a login request."""

    email: EmailStr = Field(max_length=EMAIL_MAX_LENGTH)
    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )


class LoginResponse(BaseModel):
    """Return the created token and user info"""
    access_token: str
    token_type: str
    user: UserResponse
