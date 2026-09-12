from fastapi import APIRouter
from app.services.item_service import get_all_items
from app.schemas.item import ItemResponse
from typing import List

router = APIRouter(prefix="/api/v1/items", tags=["items"])

@router.get("")
def get_items() -> List[ItemResponse]:
    return get_all_items()

