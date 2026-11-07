from typing import Any

from psycopg import Connection

from app.exceptions.item import ItemNotFoundError, PhotoNotFoundError
from app.repositories.item_repository import ItemRepository
from app.repositories.item_photo_repository import ItemPhotoRepository


# Checks item access before retrieving its photo.
class ItemPhotoService:
    def __init__(self, conn: Connection) -> None:
        self.item_repository = ItemRepository(conn)
        self.photo_repository = ItemPhotoRepository(conn)

    def get_photo(self, item_id: int) -> dict[str, Any]:
        item = self.item_repository.get_by_id(item_id)
        if item is None:
            raise ItemNotFoundError("Item not found.")

        photo = self.photo_repository.get_by_item_id(item_id)
        if photo is None:
            raise PhotoNotFoundError("Photo not found.")

        return photo
