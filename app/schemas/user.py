# BaseModel validates input data using the field types and rules we define.
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=50)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    password: str

    # Remove surrounding whitespace before validating name lengths.
    @field_validator("first_name", "last_name", mode="before")
    def strip_name_whitespace(value):
        if isinstance(value, str):
            return value.strip()
        return value
