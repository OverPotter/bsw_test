from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from src.api import router
from src.rabbit.manager import MessageQueue, connect_to_broker
from src.services.logging_service.logging_service import logger_factory

logger = logger_factory()


class AppState:
    mq: Optional[MessageQueue] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state = AppState()
    mq = MessageQueue()
    try:
        mq.channel = await connect_to_broker()
        app.state.mq = mq
        logger.info(f"MQ channel initialized: {mq.channel}")
        yield
    finally:
        await mq.close()
        logger.info("MQ channel closed")


app = FastAPI(
    title="LineProvider",
    version="0.0.1",
    docs_url="/api/v1/line-provider/docs",
    redoc_url="/api/v1/line-provider/redoc",
    openapi_url="/api/v1/line-provider/openapi.json",
    lifespan=lifespan,
)

app.include_router(router=router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
