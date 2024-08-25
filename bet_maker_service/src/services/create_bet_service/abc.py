from abc import ABC, abstractmethod

from src.schemas.payload.bets.base import BetBasePayload
from src.schemas.response.bets.base import BetBaseResponse


class AbstractCreateBetService(ABC):
    @abstractmethod
    async def create_bet(self, payload: BetBasePayload) -> BetBaseResponse: ...
