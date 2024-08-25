import asyncio
import json
import logging
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

import aio_pika
from _decimal import Decimal
from aio_pika import Channel, Message
from aio_pika.abc import AbstractRobustChannel
from pydantic import BaseModel
from src.config import settings_factory

setting = settings_factory()


class BaseRMQ:
    def __init__(self, channel: Channel = None):
        self.channel = channel

    @staticmethod
    def serialize(data: Any) -> bytes:
        def default(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            if isinstance(obj, Enum):
                return obj.name
            if isinstance(obj, BaseModel):
                return obj.dict()
            if isinstance(obj, UUID):
                return str(obj)
            raise TypeError(f"Type {type(obj)} not serializable")

        try:
            return json.dumps(data, default=default).encode()
        except TypeError as e:
            logging.error(f"Ошибка сериализации: {e}")
            raise

    @staticmethod
    def deserialize(data: bytes) -> Any:
        return json.loads(data)


class MessageQueue(BaseRMQ):

    async def send(self, queue_name: str, data: Any):
        await self.channel.declare_queue(queue_name, durable=True)
        message = Message(
            body=self.serialize(data),
            content_type="application/json",
            correlation_id=str(uuid4()),
        )
        await self.channel.default_exchange.publish(message, routing_key=queue_name)
        logging.info(f"Message sent to {queue_name}")

    async def consume_queue(
        self, func, queue_name: str, auto_delete_queue: bool = False
    ):
        queue = await self.channel.declare_queue(
            queue_name, auto_delete=auto_delete_queue, durable=True
        )

        async with queue.iterator() as queue_iter:
            logging.info("Started consuming messages...")
            async for message in queue_iter:
                logging.debug(f"Received message body: {message.body}")
                await func(message)

    async def close(self):
        if self.channel:
            logging.info("Closing MQ channel")
            await self.channel.close()
            self.channel = None


async def connect_to_broker() -> AbstractRobustChannel:
    retries = 0
    broker_connection = None
    broker_channel = None

    conn_str = f"amqp://{setting.RMQ_LOGIN}:{setting.RMQ_PASSWORD}@{setting.RMQ_HOST}:{setting.RMQ_PORT}/"

    while not broker_connection:
        logging.info(f"Trying to connect to broker: {conn_str}")
        try:
            broker_connection = await aio_pika.connect_robust(conn_str)
            logging.info(
                f"Connected to broker ({type(broker_connection)} ID {id(broker_connection)})"
            )
        except Exception as e:
            retries += 1
            logging.error(f"Can't connect to broker. Retry #{retries}. Error: {e}")
            await asyncio.sleep(5)

    if not broker_channel:
        logging.info("Trying to create channel to broker")
        broker_channel = await broker_connection.channel()
        logging.info(
            f"Channel to broker established ({type(broker_channel)} ID {id(broker_channel)})"
        )

    return broker_channel
