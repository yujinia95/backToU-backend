from typing import Any

from psycopg import Connection

from app.core.security import hash_password, verify_password
from app.exceptions.user import EmailAlreadyExistsError, InvalidCredentialsError
from app.repositories.user_repository import UserRepository
from app.schemas.login import UserLogin
from app.schemas.user import UserCreate


class UserService:
    """
    Handle user registration and login workflows.

    Coordinates user lookup and creation through UserRepository and handles
    password hashing and verification through the security module.
    """

    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.user_repository = UserRepository(self.conn)

    def signup(self, user: UserCreate) -> dict[str, Any]:
        """
        Register a user and return their public data.

        Check for an existing email, hash the raw password, insert the user,
        and commit the transaction. Return the created user's public fields,
        or roll back the insert if it fails.
        """
        existing_user = self.user_repository.get_by_email(user.email)

        if existing_user is not None:
            raise EmailAlreadyExistsError(
                "User with this email already exists."
            )

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

    def login(self, credentials: UserLogin) -> dict[str, Any]:
        """
        Verify a user's login credentials and return their public data.

        Find the user by email and compare the submitted password with the
        stored password hash. Raise the same error when either value is wrong.
        """
        existing_user = self.user_repository.get_by_email(credentials.email)

        if existing_user is None:
            raise InvalidCredentialsError("Invalid email or password.")

        password_is_valid = verify_password(
            credentials.password,
            existing_user["password_hash"],
        )

        if not password_is_valid:
            raise InvalidCredentialsError("Invalid email or password.")

        return {
            "id": existing_user["id"],
            "email": existing_user["email"],
            "first_name": existing_user["first_name"],
            "last_name": existing_user["last_name"],
        }
