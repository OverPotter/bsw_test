from pydantic import TypeAdapter
from src.database.repositories.bet_repository import BetRepository
from src.schemas.payload.bets.base import BetBasePayload
from src.schemas.response.bets.base import BetBaseResponse
from src.services.create_bet_service.abc import AbstractCreateBetService


class RepositoryCreateBetService(AbstractCreateBetService):
    def __init__(
        self,
        bet_repository: BetRepository,
    ):
        self._bet_repository = bet_repository

    async def create_bet(self, payload: BetBasePayload) -> BetBaseResponse:
        bet = await self._bet_repository.create(**payload.dict())
        return TypeAdapter(BetBaseResponse).validate_python(bet)  # type: ignore
