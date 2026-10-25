from typing import Any
from psycopg import Connection
from app.exceptions.item import UserNotFoundError
from app.repositories.user_repository import UserRepository
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemResponse
from app.schemas.match import MatchGroupResponse, MatchResponse
from app.core.matching import MatchScore

MATCH_THRESHOLD = 40

class MatchService: 
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.user_repository = UserRepository(self.conn)
        self.item_repository = ItemRepository(self.conn)
        self.match = MatchScore()
        
    def get_matches_for_user(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError("User not found.")
        
        items = self.item_repository.get_active_by_user_id(user_id)
        groups = []
        for item in items:
            candidates = self.item_repository.get_matching_candidates(item)
            
            scored = []
            for candidate in candidates:
                score, reasons = self.match.score_total(item, candidate)
                if score >= MATCH_THRESHOLD: 
                    scored.append((score, reasons, candidate))
            
            scored.sort(key=lambda s: s[0], reverse=True)
            
            matches = [
                MatchResponse(item=ItemResponse(**candidate), score=score, reasons=reasons)
                for score, reasons, candidate in scored
            ]

            group = MatchGroupResponse(
                item = ItemResponse(**item),
                matches = matches
            )
            groups.append(group)
        
            
        
        return groups
