from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.exceptions.user import InvalidUserTokenError


password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Convert a plain-text password into a secure password hash."""
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Check whether a plain-text password matches a stored password hash."""
    return password_hasher.verify(password, hashed_password)


def create_token(user_id: int) -> str:
    """Create a new token for the user"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = { 
               "sub": str(user_id),
               "exp": expire
               }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> int:
    """
    Verify the given token string and return user_id
    if it's invalid, catches the error and raise "InvalidUserTokenError"
        - jwt.decode throws: signature mismatch, expiration, wrong token form
        - payload["sub"] throws: KeyError - if key("sub") doesn't exist
        - int(...) throws: ValueError - if ... is not number
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])    
        user_id = int(payload["sub"]) # type of payload["sub"] = str
    except (KeyError, ValueError, jwt.InvalidTokenError) as error:
        raise InvalidUserTokenError from error
    return user_id
