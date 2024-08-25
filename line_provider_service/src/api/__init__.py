from fastapi import APIRouter
from src.api.events import router as event_router

router = APIRouter()

router.include_router(event_router, tags=["events"])
