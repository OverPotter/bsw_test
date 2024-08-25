import time

from fastapi import APIRouter, Depends
from src.constants import EVENTS
from src.database.repositories.manager import (
    OrmRepositoryManager,
    orm_repository_manager_factory,
)
from src.schemas.payload.bets.base import BetBasePayload
from src.schemas.response.bets.base import BetBaseResponse
from src.services.create_bet_service.abc import AbstractCreateBetService
from src.services.create_bet_service.repository import RepositoryCreateBetService
from src.services.get_bets_service.abc import AbstractGetBetsService
from src.services.get_bets_service.repository import RepositoryGetBetsService

router = APIRouter(prefix="/bet")
repository_manager = orm_repository_manager_factory()


@router.get("/events")
async def get_available_events_to_bets():
    available_events = [e for e in EVENTS.values() if time.time() < e.deadline]
    return available_events


@router.post("", response_model=BetBaseResponse)
async def create_bet(
    payload: BetBasePayload,
    repository_manager: OrmRepositoryManager = Depends(orm_repository_manager_factory),
):
    service: AbstractCreateBetService = RepositoryCreateBetService(
        bet_repository=repository_manager.get_bet_repository()
    )
    return await service.create_bet(payload=payload)


@router.get("", response_model=list[BetBaseResponse])
async def get_all_bets(
    repository_manager: OrmRepositoryManager = Depends(orm_repository_manager_factory),
):
    service: AbstractGetBetsService = RepositoryGetBetsService(
        bet_repository=repository_manager.get_bet_repository()
    )
    return await service.get_all_bets()
