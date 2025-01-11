from _decimal import Decimal
from src.schemas.response.base import BaseResponse


class BetBaseResponse(BaseResponse):
    event_id: int
    bet_amount: Decimal
