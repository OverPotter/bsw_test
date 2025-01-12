import time

from fastapi import APIRouter, HTTPException, Path, Request
from src.constants import MQ_ROUTING_KEY
from src.models import Event, events
from src.services.logging_service.logging_service import logger_factory

router = APIRouter(prefix="/event")

logger = logger_factory()


@router.put("")
async def create_event(event: Event, request: Request):
    mq = request.app.state.mq
    event_id = str(event.event_id)

    current_time = int(time.time())
    event.deadline += current_time

    is_new_event = event_id not in events

    if is_new_event:
        events[event_id] = event
        logger.debug(f"Created new event: {event}.")
    else:
        updated_fields = event.dict(exclude_unset=True)
        for field, value in updated_fields.items():
            setattr(events[event_id], field, value)
        logger.debug(f"Updated event {event_id}: {updated_fields}.")

    await mq.send(MQ_ROUTING_KEY, event)
    action = "Created" if is_new_event else "Updated"
    logger.info(
        f"{action} event with event_id {event_id} sent to {MQ_ROUTING_KEY}."
    )

    return {}


@router.get("/{event_id}")
async def get_event(event_id: str = Path(description="Event id")):
    logger.debug(
        f"""Available events: {events}
    We are looking for an event with id: {event_id}."""
    )
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail="Event not found")
