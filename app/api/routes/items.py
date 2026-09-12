from fastapi import APIRouter, HTTPException
from app.services.item_service import get_all_items, get_item_by_id
from app.schemas.item import ItemResponse
from typing import List

router = APIRouter(prefix="/api/v1/items", tags=["items"])

@router.get("")
def get_items() -> List[ItemResponse]:
    return get_all_items()

@router.get("/{id}")
def get_item(id: int) -> ItemResponse:
    try: 
        return get_item_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    