class EmailAlreadyExistsError(Exception):
    """Raised when a user tries to sign up with an existing email."""


class InvalidCredentialsError(Exception):
    """Raised when a login email or password is incorrect."""
