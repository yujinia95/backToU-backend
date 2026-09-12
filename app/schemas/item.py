from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class ItemPostRequest (BaseModel):
    user_id: int
    type: str
    date: date
    title: str
    description: Optional[str] = None
    category: str
    colors: Optional[List[str]] = None
    brand: Optional[str] = None
    location: str
    # image_key: bytea
    
class ItemUpdateRequest (BaseModel):
    type: Optional[str] = None
    status: Optional[str] = None
    date: Optional[date] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    colors: Optional[List[str]] = None
    brand: Optional[str] = None
    location: Optional[str] = None
    # image_key: bytea

# for POST, GET, PATCH
class ItemResponse (BaseModel):
    id: int
    user_id: int
    type: str
    status: str
    date: date 
    title: str
    description: Optional[str] = None
    category: str
    colors: Optional[List[str]] = None
    brand: Optional[str] = None
    location: str
    # image_key: bytea
    created_at: datetime
