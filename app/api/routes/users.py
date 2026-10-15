from typing import Annotated
from fastapi import APIRouter, Depends
from psycopg import Connection
from app.core.database import get_db

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/{user_id}/matches")
def get_matches(user_id: int, conn: Annotated[Connection, Depends(get_db)]):
    return []
