from typing import Any

from _decimal import Decimal
from src.schemas.response.base import BaseResponse


class EventBaseResponse(BaseResponse):
    event_id: int
    coefficient: Decimal
    deadline: int | float
    state: Any
