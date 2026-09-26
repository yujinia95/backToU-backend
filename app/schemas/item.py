from pydantic import BaseModel, Field, StringConstraints, field_validator
from datetime import date as date_type, datetime
from typing import Annotated, Optional, List
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
    description: Optional[str] = Field(default=None, max_length=2000)
    category: str = Field(min_length=1, max_length=50)
    colors: List[Color] = Field(min_length=1)
    brand: Optional[str] = Field(default=None, max_length=100)
    location: str = Field(min_length=1)

    @field_validator("title", "category", "location", mode="before")
    def strip_whitespace(value):
        if isinstance(value, str):
            return value.strip()
        return value

class ItemUpdateRequest(BaseModel):
    type: Optional[ItemType] = Field(default=None)
    status: Optional[ItemStatus] = Field(default=None)
    date: Optional[date_type] = None
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=2000)
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    colors: Optional[List[Color]] = Field(default=None, min_length=1)
    brand: Optional[str] = Field(default=None, max_length=100)
    location: Optional[str] = Field(default=None, min_length=1)

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
    description: Optional[str] = None
    category: str
    colors: List[Color]
    brand: Optional[str] = None
    location: str
    created_at: datetime

class ItemPosterResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

class ItemDetailResponse(ItemResponse):
    poster: ItemPosterResponse
