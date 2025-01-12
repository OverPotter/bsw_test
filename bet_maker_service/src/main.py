import asyncio
import json
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from src.api import router
from src.constants import MQ_ROUTING_KEY
from src.rabbit.manager import MessageQueue, connect_to_broker
from src.schemas.response.events.base import EventBaseResponse
from src.services.logging_service.logging_service import logger_factory

logger = logger_factory()


class AppState:
    mq: Optional[MessageQueue] = None
    events: dict[int, EventBaseResponse] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state = AppState()
    mq = MessageQueue()
    try:
        mq.channel = await connect_to_broker()
        app.state.mq = mq
        logger.info(f"MQ channel initialized: {mq.channel}")

        async def mq_accept_message(message):
            event_data = json.loads(message.body)
            event = EventBaseResponse(**event_data)

            app.state.events[event.event_id] = event

            logger.info(f"Event stored in memory: {event}")
            await message.ack()

        asyncio.create_task(mq.consume_queue(mq_accept_message, MQ_ROUTING_KEY))

        yield
    finally:
        await mq.close()
        logger.info("MQ channel closed")


app = FastAPI(
    title="BetMaker",
    version="0.0.1",
    docs_url="/api/v1/bet-maker/docs",
    redoc_url="/api/v1/bet-maker/redoc",
    openapi_url="/api/v1/bet-maker/openapi.json",
    lifespan=lifespan,
)

app.include_router(router=router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
