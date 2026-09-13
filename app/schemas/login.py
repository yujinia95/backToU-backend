"""Request schema for user login."""

from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    """Validate the email and password received in a login request."""

    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8, max_length=128)
