from psycopg import Connection

from app.exceptions.conversation import ConversationNotFoundError, NotConversationMemberError
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.conversation_repository = ConversationRepository(self.conn)

    def check_membership(self, conversation_id: int, user_id: int) -> None:
        """Raise if the conversation does not exist or the user is not in it."""
        conversation = self.conversation_repository.get_by_id(conversation_id)

        # no such conversation
        if conversation is None:
            raise ConversationNotFoundError("Conversation not found.")

        # the user is neither the founder nor the claimant
        if user_id != conversation["founder_id"] and user_id != conversation["claimant_id"]:
            raise NotConversationMemberError("You are not a member of this conversation.")