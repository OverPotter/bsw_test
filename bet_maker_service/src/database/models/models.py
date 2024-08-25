from _decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from src.database.models._universal_type_annotations import uuid
from src.database.models.base import BaseIDModel


class BetModel(BaseIDModel):
    __tablename__ = "bet"

    event_id: Mapped[uuid] = mapped_column(nullable=False)
    bet_amount: Mapped[Decimal] = mapped_column(nullable=False)
