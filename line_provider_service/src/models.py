import time
from enum import Enum
from typing import Optional

from _decimal import Decimal
from pydantic import BaseModel


class EventState(Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class Event(BaseModel):
    event_id: int
    coefficient: Optional[Decimal] = None
    deadline: Optional[int] = None
    state: Optional[EventState] = None


events: dict[str, Event] = {
    "1": Event(
        event_id=1,
        coefficient=Decimal("1.2"),
        deadline=int(time.time()) + 600,
        state=EventState.NEW,
    ),
    "2": Event(
        event_id=2,
        coefficient=Decimal("1.15"),
        deadline=int(time.time()) + 60,
        state=EventState.NEW,
    ),
    "3": Event(
        event_id=3,
        coefficient=Decimal("1.67"),
        deadline=int(time.time()) + 90,
        state=EventState.NEW,
    ),
}
