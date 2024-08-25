from abc import ABC, abstractmethod

from src.schemas.response.bets.base import BetBaseResponse


class AbstractGetBetsService(ABC):
    @abstractmethod
    async def get_all_bets(self) -> list[BetBaseResponse]: ...
