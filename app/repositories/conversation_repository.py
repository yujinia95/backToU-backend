from typing import Any
from psycopg import Connection

class ConversationRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def get_by_id(self, conversation_id: int) -> dict[str, Any] | None:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, item_id, founder_id, claimant_id
                FROM conversations AS c
                WHERE c.id = %s
                """,
                (conversation_id,),
            )
            return cursor.fetchone()