from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import Response
from psycopg import Connection

from app.core.database import get_db
from app.core.photos import MAX_PHOTO_BYTES
from app.exceptions.item import (
    EmptyUpdateError,
    InvalidPhotoError,
    InvalidUpdateError,
    ItemNotFoundError,
    NotItemOwnerError,
    PhotoNotFoundError,
    PhotoTooLargeError,
)
from app.schemas.item import (
    ItemDetailResponse,
    ItemPhotoResponse,
    ItemPostRequest,
    ItemResponse,
    ItemUpdateRequest,
)
from app.services.item_service import ItemService
from app.services.item_photo_service import ItemPhotoService
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


@router.get("/{id}/photo", response_class=Response)
def get_item_photo(
    id: int,
    conn: Annotated[Connection, Depends(get_db)],
) -> Response:
    service = ItemPhotoService(conn)

    try:
        photo = service.get_photo(id)
    except (ItemNotFoundError, PhotoNotFoundError) as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    return Response(
        content=photo["image_data"],
        media_type=photo["content_type"],
        headers={"Cache-Control": "no-store"},
    )


@router.put("/{id}/photo")
def upload_item_photo(
    id: int,
    photo: Annotated[UploadFile, File()],
    conn: Annotated[Connection, Depends(get_db)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> ItemPhotoResponse:
    service = ItemPhotoService(conn)

    try:
        image_data = photo.file.read(MAX_PHOTO_BYTES + 1)
        saved_photo = service.save_photo(
            id,
            current_user["id"],
            image_data,
        )
    except ItemNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except NotItemOwnerError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except PhotoTooLargeError as error:
        raise HTTPException(status_code=413, detail=str(error)) from error
    except InvalidPhotoError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return ItemPhotoResponse(**saved_photo)


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
