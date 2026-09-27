from pydantic import BaseModel, Field, StringConstraints, field_validator
from datetime import date as date_type, datetime
from typing import Annotated, List
from enum import Enum

Color = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=20),
]

class ItemType(str, Enum):
    LOST = "lost"
    FOUND = "found"

class ItemStatus(str, Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    
class ItemPostRequest(BaseModel):
    user_id: int
    type: ItemType
    date: date_type
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=2000)
    category: str = Field(min_length=1, max_length=50)
    colors: List[Color] = Field(min_length=1)
    brand: str | None = Field(default=None, max_length=100)
    location: str = Field(min_length=1)

    @field_validator("title", "category", "location", mode="before")
    def strip_whitespace(value):
        if isinstance(value, str):
            return value.strip()
        return value

class ItemUpdateRequest(BaseModel):
    type: ItemType | None = Field(default=None)
    status: ItemStatus | None = Field(default=None)
    date: date_type | None = None
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=2000)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    colors: List[Color] | None = Field(default=None, min_length=1)
    brand: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, min_length=1)

    @field_validator("title", "category", "location", mode="before")
    def strip_whitespace(value):
        if isinstance(value, str):
            return value.strip()
        return value

# for POST, GET, PATCH
class ItemResponse(BaseModel):
    id: int
    user_id: int
    type: ItemType
    status: ItemStatus
    date: date_type
    title: str
    description: str | None = None
    category: str
    colors: List[Color]
    brand: str | None = None
    location: str
    created_at: datetime
    # Set by the server when status becomes "returned"; never accepted from clients.
    returned_at: datetime | None = None

class ItemPosterResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

class ItemDetailResponse(ItemResponse):
    poster: ItemPosterResponse
