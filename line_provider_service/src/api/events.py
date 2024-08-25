from fastapi import APIRouter, HTTPException, Path, Request
from src.constants import MQ_ROUTING_KEY
from src.models import Event, events

router = APIRouter(prefix="/event")


@router.put("")
async def create_event(event: Event, request: Request):
    mq = request.app.state.mq

    if event.event_id not in events:
        events[event.event_id] = event
        return {}

    for p_name, p_value in event.dict(exclude_unset=True).items():
        setattr(events[event.event_id], p_name, p_value)

    await mq.send(MQ_ROUTING_KEY, event)

    return {}


@router.get("/{event_id}")
async def get_event(event_id: str = Path(description="Event id")):
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail="Event not found")
