class ConversationNotFoundError(Exception):
    """Raised when no conversation exists with the given id."""


class NotConversationMemberError(Exception):
    """Raised when the user is neither the founder nor the claimant of the conversation."""