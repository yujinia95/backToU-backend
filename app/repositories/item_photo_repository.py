from typing import Any

from psycopg import Connection


# Handles database storage for item photos.
class ItemPhotoRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def save(
        self,
        item_id: int,
        image_data: bytes,
        content_type: str,  # e.g. "image/jpeg" or "image/png"
    ) -> dict[str, Any]:
        """Insert a photo or replace the item's existing photo."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO item_photos (
                    item_id, image_data, content_type
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (item_id)
                DO UPDATE SET
                    image_data = EXCLUDED.image_data,
                    content_type = EXCLUDED.content_type,
                    updated_at = NOW()
                RETURNING id, item_id, content_type, updated_at
                """,
                (item_id, image_data, content_type),
            )
            photo = cursor.fetchone()

        if photo is None:
            raise RuntimeError("Database did not return the saved photo")

        return photo

    def get_by_item_id(self, item_id: int) -> dict[str, Any] | None:
        """Fetch the item's photo, or return None if it has no photo."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, item_id, image_data, content_type, updated_at
                FROM item_photos
                WHERE item_id = %s
                """,
                (item_id,),
            )
            return cursor.fetchone()
