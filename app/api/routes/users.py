from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from psycopg import Connection
from app.core.database import get_db
from app.services.match_service import MatchService
from app.exceptions.item import UserNotFoundError

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/{user_id}/matches")
def get_matches(user_id: int, conn: Annotated[Connection, Depends(get_db)]) -> list[MatchGroupResponse]:
    service = MatchService(conn)
    try:
        return service.get_matches_for_user(user_id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
