from typing import Annotated, Any
from fastapi import APIRouter, Depends
from psycopg import Connection
from app.core.database import get_db
from app.services.match_service import MatchService
from app.schemas.match import MatchGroupResponse
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/matches")
def get_matches(
    conn: Annotated[Connection, Depends(get_db)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> list[MatchGroupResponse]:
    service = MatchService(conn)
    return service.get_matches_for_user(current_user["id"])
