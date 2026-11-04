from typing import Any

from psycopg import Connection

from app.core.security import hash_password, verify_password, create_token, verify_token
from app.exceptions.user import EmailAlreadyExistsError, InvalidCredentialsError, TokenUserNotFoundError
from app.repositories.user_repository import UserRepository
from app.schemas.login import UserLogin
from app.schemas.user import UserCreate


class UserService:
    """
    Handle user registration, login workflows, and token verification.

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
        Verify a user's login credentials 
        and return their public data with token.

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
        
        access_token = create_token(existing_user["id"])
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": existing_user["id"],
                "email": existing_user["email"],
                "first_name": existing_user["first_name"],
                "last_name": existing_user["last_name"],
            }  
        }
    
    def get_current_user(self, token: str) -> dict[str, Any]:
        """
        Verify if the token is valid and find the corresponding user info from DB
        """
        user_id = verify_token(token)
        user_info = self.user_repository.get_by_id(user_id)
        
        if user_info is None:
            raise TokenUserNotFoundError("Invalid User")
        
        return user_info
