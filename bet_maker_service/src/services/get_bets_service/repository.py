from pydantic import TypeAdapter
from src.database.repositories.bet_repository import BetRepository
from src.schemas.response.bets.base import BetBaseResponse
from src.services.get_bets_service.abc import AbstractGetBetsService


class RepositoryGetBetsService(AbstractGetBetsService):
    def __init__(
        self,
        bet_repository: BetRepository,
    ):
        self._bet_repository = bet_repository

    async def get_all_bets(self) -> list[BetBaseResponse]:
        bets = await self._bet_repository.get_all()
        return [TypeAdapter(BetBaseResponse).validate_python(bet) for bet in bets]  # type: ignore
