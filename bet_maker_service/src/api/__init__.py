from fastapi import APIRouter
from src.api.bets import router as bet_router

router = APIRouter()

router.include_router(bet_router, tags=["bets"])
