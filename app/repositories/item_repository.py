from typing import Any
from psycopg import Connection

class ItemRepository:
    """
    Data access layer for item entities.

    Encapsulates database operations for the 'items' table.
    """

    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def create(
        self,
        *,
        user_id: int,
        type_: str,
        date_,
        title: str,
        description: str | None,
        category: str,
        colors: list[str] | None,
        brand: str | None,
        location: str,
    ) -> dict[str, Any]:
        """Insert an item row and return its public fields."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO items (user_id, type, date, title, description, category, colors, brand, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, user_id, type, status, date, title, description, category, colors, brand, location, created_at
                """,
                (user_id, type_, date_, title, description, category, colors, brand, location),
            )
            created_item = cursor.fetchone()

        if created_item is None:
            raise RuntimeError("Database did not return the created item")

        return created_item

    def get_by_id(self, item_id: int) -> dict[str, Any] | None:
        """Fetch an item row by id, or return None."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, user_id, type, status, date, title, description, category, colors, brand, location, created_at
                FROM items
                WHERE id = %s
                """,
                (item_id,),
            )
            return cursor.fetchone()

    def get_all(self) -> list[dict[str, Any]]:
        """Fetch all item rows."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, user_id, type, status, date, title, description, category, colors, brand, location, created_at
                FROM items
                """
            )
            return cursor.fetchall()

    def update(self, item_id: int, set_clause_str: str, values: list) -> dict[str, Any] | None:
        """Update specific fields on an item row and return the updated row, or None if not found."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE items
                SET {set_clause_str}
                WHERE id = %s
                RETURNING id, user_id, type, status, date, title, description, category, colors, brand, location, created_at
                """,
                values + [item_id],
            )
            return cursor.fetchone()

    def delete(self, item_id: int) -> int:
        """Delete an item row by id. Returns the number of rows affected."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM items
                WHERE id = %s
                """,
                (item_id,),
            )
            return cursor.rowcount
