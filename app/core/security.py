from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Convert a plain-text password into a secure password hash."""
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Check whether a plain-text password matches a stored password hash."""
    return password_hasher.verify(password, hashed_password)
