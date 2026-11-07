from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from psycopg import Connection

from app.core.database import get_db
from app.exceptions.item import EmptyUpdateError, ItemNotFoundError, InvalidUpdateError, NotItemOwnerError
from app.schemas.item import ItemDetailResponse, ItemPostRequest, ItemResponse, ItemUpdateRequest
from app.services.item_service import ItemService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_item_endpoint(
    data: ItemPostRequest,
    conn: Annotated[Connection, Depends(get_db)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> ItemResponse:
    """
    Handles item creation request 
    """
    service = ItemService(conn)
    return service.create_item(data, current_user["id"])


@router.get("")
def get_items(conn: Annotated[Connection, Depends(get_db)]) -> list[ItemResponse]:
    service = ItemService(conn)
    return service.get_all_items()


@router.get("/{id}")
def get_item(id: int, conn: Annotated[Connection, Depends(get_db)]) -> ItemDetailResponse:
    service = ItemService(conn)
    try:
        return service.get_item_by_id(id)
    except ItemNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.patch("/{id}") #item id
def update_item_endpoint(
    id: int,
    data: ItemUpdateRequest,
    conn: Annotated[Connection, Depends(get_db)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> ItemResponse:
    service = ItemService(conn)
    try:
        return service.update_item(id, data, current_user["id"])
    except ItemNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except (EmptyUpdateError, InvalidUpdateError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except NotItemOwnerError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_endpoint(
    id: int,
    conn: Annotated[Connection, Depends(get_db)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],):
    service = ItemService(conn)
    try:
        service.delete_item(id,current_user["id"])
    except ItemNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except NotItemOwnerError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
