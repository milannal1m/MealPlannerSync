from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
import asyncio
from db import get_db
from rabbitmq import start_sync_queue, start_websocket_queue, send_notification
from crud import create_user, get_user_connections, create_connection, delete_connection

app = FastAPI(root_path="/user")

asyncio.create_task(start_sync_queue())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await start_websocket_queue(websocket)
    
@app.post("/users")
def create_user_endpoint(username: str, db: Session = Depends(get_db)):
    return create_user(username, db)

@app.get("/users/{username}/connections")
def get_user_connections_endpoint(username: str, db: Session = Depends(get_db)):
    return get_user_connections(username, db)

@app.post("/users/{username}/connections")
async def create_connection_endpoint(username: str, connected_username: str, db: Session = Depends(get_db)):
    new_connection = await create_connection(username, connected_username, db)
    await send_notification(f"New Connection {new_connection['user1']} - {new_connection['user2']}")
    return new_connection

@app.delete("/users/{username}/connections/{connected_username}")
async def delete_connection_endpoint(username: str, connected_username: str, db: Session = Depends(get_db)):
    response = delete_connection(username, connected_username, db)
    await send_notification(f"Connection Deleted {username} - {connected_username}")
    return response