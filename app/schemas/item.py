from pydantic import BaseModel, Field, StringConstraints, field_validator, model_validator
from datetime import date as date_type, datetime
from typing import Annotated, Any
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

# Mirrors the options offered by the frontend's category dropdown.
class ItemCategory(str, Enum):
    BAGS = "Bags"
    CLOTHING = "Clothing"
    ELECTRONICS = "Electronics"
    KEYS = "Keys"
    JEWELRY = "Jewelry"
    ACCESSORIES = "Accessories"
    SPORTS = "Sports"
    DOCUMENTS = "Documents"
    OTHER = "Other"
    
class ItemPostRequest(BaseModel):
    type: ItemType
    date: date_type
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=2000)
    category: ItemCategory
    colors: list[Color] = Field(min_length=1)
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
    category: ItemCategory | None = Field(default=None)
    colors: list[Color] | None = Field(default=None, min_length=1)
    brand: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, min_length=1)

    @field_validator("title", "category", "location", mode="before")
    def strip_whitespace(value):
        if isinstance(value, str):
            return value.strip()
        return value

# Kept in step with the items router's prefix.
PHOTO_URL_PREFIX = "/api/v1/items"


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
    colors: list[Color]
    brand: str | None = None
    location: str
    created_at: datetime
    # Set by the server when status becomes "returned"; never accepted from clients.
    returned_at: datetime | None = None
    # Where to fetch this item's photo, or None when it has none. Built by the
    # server so clients never assemble the path themselves: pointing this at
    # object storage later requires no change on their side.
    photo_url: str | None = None

    @model_validator(mode="before")
    @classmethod
    def derive_photo_url(cls, data: Any) -> Any:
        """Turn the joined photo timestamp into a URL the client can request.

        The timestamp rides along as a query parameter so that replacing a photo
        changes its URL, and a cached copy of the old one is never reused.
        """
        if not isinstance(data, dict) or data.get("photo_url") is not None:
            return data

        photo_updated_at = data.get("photo_updated_at")
        if photo_updated_at is None:
            return data

        data = dict(data)
        version = int(photo_updated_at.timestamp())
        data["photo_url"] = f"{PHOTO_URL_PREFIX}/{data['id']}/photo?v={version}"
        return data

class ItemPosterResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

class ItemDetailResponse(ItemResponse):
    poster: ItemPosterResponse


class ItemPhotoResponse(BaseModel):
    id: int
    item_id: int
    content_type: str
    updated_at: datetime
