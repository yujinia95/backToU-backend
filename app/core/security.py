from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings


password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Convert a plain-text password into a secure password hash."""
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Check whether a plain-text password matches a stored password hash."""
    return password_hasher.verify(password, hashed_password)

def create_token(user_id: int) -> str:
    """Create a bew token for the user"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = { 
               "sub": str(user_id),
               "exp": expire
               }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    
    
