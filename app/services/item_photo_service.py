from typing import Any

from psycopg import Connection

from app.core.photos import validate_photo
from app.exceptions.item import ItemNotFoundError, NotItemOwnerError, PhotoNotFoundError
from app.repositories.item_repository import ItemRepository
from app.repositories.item_photo_repository import ItemPhotoRepository


# Coordinates item photo access, validation, and storage.
class ItemPhotoService:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
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

    def save_photo(
        self,
        item_id: int,
        user_id: int,
        image_data: bytes,
    ) -> dict[str, Any]:
        """Validate and save a photo for an item owned by the user."""
        try:
            item = self.item_repository.get_by_id(item_id)
            if item is None:
                raise ItemNotFoundError("Item not found.")

            if item["user_id"] != user_id:
                raise NotItemOwnerError(
                    "You do not have permission to change this photo."
                )

            content_type = validate_photo(image_data)

            photo = self.photo_repository.save(
                item_id,
                image_data,
                content_type,
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

        return photo
