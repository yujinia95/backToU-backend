"""
HTTP layer for the health check.
"""
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}