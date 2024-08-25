from uuid import UUID

from _decimal import Decimal
from src.schemas.payload.base import BasePayload


class BetBasePayload(BasePayload):
    event_id: UUID
    bet_amount: Decimal
