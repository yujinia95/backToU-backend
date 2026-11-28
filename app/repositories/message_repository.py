from typing import Any
from psycopg import Connection


class MessageRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def create(self, conversation_id: int, sender_id: int, content: str) -> dict[str, Any]:
        """Insert a message and return the saved row."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO messages (conversation_id, sender_id, content)
                VALUES (%s, %s, %s)
                RETURNING id, conversation_id, sender_id, content, created_at
                """,
                (conversation_id, sender_id, content),
            )
            return cursor.fetchone()