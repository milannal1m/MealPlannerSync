import uuid
import json
import asyncio
import aio_pika

RABBITMQ_HOST = "amqp://guest:guest@rabbitmq/"

async def send_request(routing_key: str, payload: dict):
    """Sendet eine Nachricht an RabbitMQ und wartet asynchron auf die Antwort."""
    connection = await aio_pika.connect_robust(RABBITMQ_HOST)
    async with connection:
        channel = await connection.channel()
        callback_queue = await channel.declare_queue(exclusive=True)

        corr_id = str(uuid.uuid4())
        future_response = asyncio.Future()

        async def on_response(message: aio_pika.IncomingMessage):
            if message.correlation_id == corr_id:
                future_response.set_result(json.loads(message.body))

        await callback_queue.consume(on_response)

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode(),
                correlation_id=corr_id,
                reply_to=callback_queue.name
            ),
            routing_key=routing_key
        )

        response = await future_response
        return response

async def send_user_request(username: str):
    """Spezialisierte Funktion für Benutzeranfragen."""
    payload = {"username": username}
    return await send_request("user_request", payload)

async def send_meal_request(username: str):
    """Spezialisierte Funktion für Mahlzeitenanfragen."""
    payload = {"username": username}
    return await send_request("meal_request", payload)