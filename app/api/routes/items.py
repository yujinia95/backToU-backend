from fastapi import APIRouter, HTTPException,status
from app.services.item_service import create_item as create_item_service, update_item as update_item_service, delete_item as delete_item_service, get_all_items, get_item_by_id
from app.schemas.item import ItemPostRequest, ItemResponse, ItemUpdateRequest
from typing import List

router = APIRouter(prefix="/api/v1/items", tags=["items"])

@router.post("")
def create_item(data: ItemPostRequest) -> ItemResponse:
    return create_item_service(data)

@router.get("")
def get_items() -> List[ItemResponse]:
    return get_all_items()

@router.get("/{id}")
def get_item(id: int) -> ItemResponse:
    try: 
        return get_item_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{id}")
def update_item(id: int, data: ItemUpdateRequest) -> ItemResponse:
    try:
        return update_item_service(id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_endpoint(id: int):
    try:
        delete_item_service(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
