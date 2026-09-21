# BaseModel validates input data using the field types and rules we define.
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.constants import (
    EMAIL_MAX_LENGTH,
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
)


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=EMAIL_MAX_LENGTH)
    first_name: str = Field(
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
    )
    last_name: str = Field(
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
    )
    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )

    # Remove surrounding whitespace before validating name lengths.
    @field_validator("first_name", "last_name", mode="before")
    def strip_name_whitespace(value):
        if isinstance(value, str):
            return value.strip()
        return value


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
