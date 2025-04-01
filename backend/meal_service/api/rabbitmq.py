import aio_pika
import asyncio
import json
from fastapi import WebSocket
from aio_pika import Message, DeliveryMode, connect_robust
from functools import partial
from db import get_db
from crud import get_user_meals
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv('RABBITMQ_URL')

async def get_rabbitmq_connection():
    """Stellt eine Verbindung zu RabbitMQ her."""
    return await connect_robust(RABBITMQ_URL)


async def send_notification(message: str):
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    exchange = await channel.declare_exchange("notifications", aio_pika.ExchangeType.FANOUT)

    await exchange.publish(
        Message(message.encode(), delivery_mode=DeliveryMode.PERSISTENT),
        routing_key=""
    )
    await connection.close()

async def start_websocket_queue(websocket: WebSocket):
    await websocket.accept()

    connection = await get_rabbitmq_connection()
    channel = await connection.channel() 
    exchange = await channel.declare_exchange("notifications", aio_pika.ExchangeType.FANOUT)
    queue = await channel.declare_queue("", exclusive=True)
    await queue.bind(exchange)

    async for message in queue:
        async with message.process():
            await websocket.send_text(message.body.decode())
    await connection.close()

async def on_sync_request(message: aio_pika.IncomingMessage, connection: aio_pika.Connection):
    """Verarbeitet eingehende Anfragen aus RabbitMQ."""
    async with message.process():
        request_data = json.loads(message.body)
        username = request_data.get("username", "unknown")
        response = get_user_meals(username, next(get_db()))
        response_data = json.dumps(
            [{"id": meal.id, "name": meal.name, "planned_for": meal.planned_for.isoformat()} for meal in response]
        )

        async with connection.channel() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=response_data.encode(),
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )

async def start_sync_queue():
    """Startet die Queue zum Verarbeiten von Meal-Requests."""
    retries = 5
    while retries > 0:
        try:
            connection = await get_rabbitmq_connection()
            channel = await connection.channel()
            queue = await channel.declare_queue("meal_request")
            callback = partial(on_sync_request, connection=connection)
            await queue.consume(callback)
            await asyncio.Future()
            break
        except aio_pika.exceptions.AMQPConnectionError:
            await asyncio.sleep(5)
            retries -= 1
