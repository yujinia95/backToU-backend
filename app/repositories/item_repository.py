from typing import Any
from psycopg import Connection
from app.schemas.item import ItemType

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
        colors: list[str],
        brand: str | None,
        location: str,
    ) -> dict[str, Any]:
        """Insert an item row and return its public fields."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO items (user_id, type, date, title, description, category, colors, brand, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, user_id, type, status, date, title, description, category, colors, brand, location, created_at, returned_at
                """,
                (user_id, type_, date_, title, description, category, colors, brand, location),
            )
            created_item = cursor.fetchone()

        if created_item is None:
            raise RuntimeError("Database did not return the created item")

        return created_item

    def get_by_id(self, item_id: int) -> dict[str, Any] | None:
        """Fetch an item and its poster by id, or return None."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    i.id,
                    i.user_id,
                    i.type,
                    i.status,
                    i.date,
                    i.title,
                    i.description,
                    i.category,
                    i.colors,
                    i.brand,
                    i.location,
                    i.created_at,
                    i.returned_at,
                    u.id AS poster_id,
                    u.first_name AS poster_first_name,
                    u.last_name AS poster_last_name
                FROM items AS i
                JOIN users AS u ON u.id = i.user_id
                WHERE i.id = %s
                """,
                (item_id,),
            )
            return cursor.fetchone()

    def get_all(self) -> list[dict[str, Any]]:
        """Fetch all item rows."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, user_id, type, status, date, title, description, category, colors, brand, location, created_at, returned_at
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
                RETURNING id, user_id, type, status, date, title, description, category, colors, brand, location, created_at, returned_at
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
        
    def get_active_by_user_id(self, user_id:int) -> list[dict[str, Any]]:
        """Fetch list of all active items by user_id, or return []."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, user_id, type, status, date, title, description, category, colors, brand, location, created_at, returned_at
                FROM items
                WHERE user_id = %s AND status = 'active'
                """,
                (user_id,),
                
            )
            return cursor.fetchall()
    
    def get_matching_candidates(self, item) -> list[dict[str, Any]]:
        """Fetch list of matching candidates
            - different user_id
            - status == active
            - opposite type 
            - for a lost item, candidate found items dated on or after it, and vice versa.
        """
        if item["type"] == ItemType.LOST: operator = ">="
        else: operator = "<="
        
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT id, user_id, type, status, date, title, description, category, colors, brand, location, created_at, returned_at
                FROM items
                WHERE user_id != %s
                AND status = 'active'
                AND type != %s
                AND date {operator} %s 
                """,
                (item["user_id"], item["type"], item["date"]),
            )
            return cursor.fetchall()
        

