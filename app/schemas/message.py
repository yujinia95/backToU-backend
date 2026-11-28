from datetime import datetime
from pydantic import BaseModel


class MessageResponse(BaseModel):
    """A saved chat message, as sent to clients."""
    id: int
    conversation_id: int
    sender_id: int
    content: str
    created_at: datetime