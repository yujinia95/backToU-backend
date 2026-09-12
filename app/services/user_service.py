from typing import Any

from psycopg import Connection

from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    """
    Handle user registration workflows.

    Checks email uniqueness, hashes raw passwords, and coordinates
    user creation via the UserRepository.
    """

    def __init__(self, conn: Connection) -> None:
        """Initialize the service and repository with one DB connection."""
        self.conn = conn
        self.user_repository = UserRepository(self.conn)
        

    def signup(self, user: UserCreate) -> dict[str, Any]:
        """
        Register a user and return fields that are safe for an API response.

        Check for an existing email, hash the raw password, insert the user,
        and commit the transaction. Roll back the insert if it fails.
        """
        existing_user = self.user_repository.get_by_email(user.email)

        if existing_user is not None:
            raise ValueError("User with this email already exists.")

        hashed_password = hash_password(user.password)

        try:
            created_user = self.user_repository.create_user(
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                password_hash=hashed_password,
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

        return created_user
