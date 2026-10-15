from typing import Any
from psycopg import Connection
from app.exceptions.item import UserNotFoundError
from app.repositories.user_repository import UserRepository

class MatchService: 
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.user_repository = UserRepository(self.conn)
        
    def get_matches_for_user(self, user_id: int):
        row = self.user_repository.get_by_id(user_id)
        if row is None:
            raise UserNotFoundError("User not found.")
        return []
