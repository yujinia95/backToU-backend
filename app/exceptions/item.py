class ItemNotFoundError(Exception):
    """Raised when an item with the given id does not exist."""


class EmptyUpdateError(Exception):
    """Raised when an update request contains no fields to update."""


class UserNotFoundError(Exception):
    """Raised when the user_id referenced by an item does not exist."""
