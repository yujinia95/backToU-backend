from pydantic import BaseModel
from app.schemas.item import ItemResponse

class MatchResponse(BaseModel):
    item: ItemResponse
    score: int
    reasons: list[str]
    
class MatchGroupResponse(BaseModel):
    item: ItemResponse
    matches: list[MatchResponse]
