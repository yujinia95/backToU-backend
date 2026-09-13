from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from psycopg import Connection

from app.core.database import get_db
from app.exceptions.item import EmptyUpdateError, ItemNotFoundError, UserNotFoundError
from app.schemas.item import ItemPostRequest, ItemResponse, ItemUpdateRequest
from app.services.item_service import ItemService

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_item_endpoint(
    data: ItemPostRequest,
    conn: Annotated[Connection, Depends(get_db)],
) -> ItemResponse:
    service = ItemService(conn)
    try:
        return service.create_item(data)
    except UserNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("")
def get_items(conn: Annotated[Connection, Depends(get_db)]) -> List[ItemResponse]:
    service = ItemService(conn)
    return service.get_all_items()


@router.get("/{id}")
def get_item(id: int, conn: Annotated[Connection, Depends(get_db)]) -> ItemResponse:
    service = ItemService(conn)
    try:
        return service.get_item_by_id(id)
    except ItemNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.patch("/{id}")
def update_item_endpoint(
    id: int,
    data: ItemUpdateRequest,
    conn: Annotated[Connection, Depends(get_db)],
) -> ItemResponse:
    service = ItemService(conn)
    try:
        return service.update_item(id, data)
    except ItemNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except EmptyUpdateError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_endpoint(id: int, conn: Annotated[Connection, Depends(get_db)]):
    service = ItemService(conn)
    try:
        service.delete_item(id)
    except ItemNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
