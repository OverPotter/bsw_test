import asyncio
import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.api import router
from src.constants import EVENTS, MQ_ROUTING_KEY
from src.rabbit.manager import MessageQueue, connect_to_broker
from src.schemas.response.events.base import EventBaseResponse


async def mq_accept_message(message):
    event_data = json.loads(message.body)
    event = EventBaseResponse(**event_data)

    EVENTS[event.event_id] = event

    logging.info(f"Processed event: {event}")
    await message.ack()


@asynccontextmanager
async def lifespan(app: FastAPI):
    mq = MessageQueue()
    try:
        mq.channel = await connect_to_broker()
        app.state.mq = mq
        logging.info(f"MQ channel initialized: {mq.channel}")

        asyncio.create_task(mq.consume_queue(mq_accept_message, MQ_ROUTING_KEY))

        yield
    finally:
        await mq.close()
        logging.info("MQ channel closed")


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

    uvicorn.run(
        "bet_maker_service.src.main:app", host="0.0.0.0", port=8080, reload=True
    )
