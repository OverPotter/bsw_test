from uuid import UUID

from _decimal import Decimal
from src.schemas.response.base import BaseResponse


class BetBaseResponse(BaseResponse):
    event_id: UUID
    bet_amount: Decimal
