"""HTTP routes for user authentication."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from psycopg import Connection

from app.core.database import get_db
from app.exceptions.user import EmailAlreadyExistsError
from app.schemas.user import UserCreate
from app.services.user_service import UserService


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
def signup(
    user: UserCreate,
    conn: Annotated[Connection, Depends(get_db)],
) -> Response:
    """
    Handle a sign-up request using validated user data.

    Delegate account creation to UserService, translate a duplicate email
    into an HTTP 409 response, and return an empty HTTP 201 response when
    the account is created successfully.
    """

    service = UserService(conn)

    try:
        service.signup(user)
    except EmailAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return Response(status_code=status.HTTP_201_CREATED)
