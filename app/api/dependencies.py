from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from psycopg import Connection

from app.core.database import get_db
from app.services.user_service import UserService
from app.exceptions.user import TokenUserNotFoundError, InvalidUserTokenError


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    conn: Annotated[Connection, Depends(get_db)],
) -> dict[str, Any]:
    """
    Return the user identified by the request's Bearer token.

    Read the token from the Authorization header and delegate verification and user lookup to UserService. 
    Translate a missing header, an invalid or expired token, and a deleted user into the same HTTP 401 response.
    Use this with Depends on routes that require a logged-in user.
    """
    
    if credentials is None:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    try:
        user_info = UserService(conn).get_user_from_token(credentials.credentials)
    except (TokenUserNotFoundError, InvalidUserTokenError) as error:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authenticated",
        ) from error
        
    return user_info
