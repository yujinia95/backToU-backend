from typing import Any
from psycopg import Connection
from app.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.message_repository = MessageRepository(self.conn)

    def save_message(self, conversation_id: int, sender_id: int, content: str) -> dict[str, Any] | None:
        """Save a message and return the stored row, or None when it is blank."""
        content = content.strip()
        # if content is empty → return None
        if not content:
            return None

        try:
            # save with the repository and keep the returned row
            saved = self.message_repository.create(conversation_id, sender_id, content)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

        # return the saved row
        return saved