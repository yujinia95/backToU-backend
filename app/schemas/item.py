from pydantic import BaseModel, Field, field_validator
from datetime import date as date_type, datetime
from typing import Optional, List
from enum import Enum

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
    colors: Optional[List[str]] = None
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
    colors: Optional[List[str]] = None
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
    colors: Optional[List[str]] = None
    brand: Optional[str] = None
    location: str
    created_at: datetime
