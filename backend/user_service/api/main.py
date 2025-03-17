from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functools import partial
import os
from dotenv import load_dotenv
import aio_pika
import asyncio
import json

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')
load_dotenv()

postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_user = os.getenv("POSTGRES_USER")

db_url = f"postgresql://{postgres_user}:{postgres_password}@user-postgres:5432/user_db"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class UserConnection(Base):
    __tablename__ = "user_connections"
    user1_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user2_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

app = FastAPI(root_path="/user")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
def create_user(username: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.name == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(name=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "name": new_user.name}

def get_connections_for_user(username: str, db: Session):
    user = db.query(User).filter(User.name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    connections = db.query(UserConnection).filter(
        (UserConnection.user1_id == user.id) | (UserConnection.user2_id == user.id)
    ).all()
    
    connected_user_ids = {conn.user1_id if conn.user2_id == user.id else conn.user2_id for conn in connections}
    connected_users = db.query(User).filter(User.id.in_(connected_user_ids)).all()
    
    return connected_users


@app.get("/users/{username}/connections")
def get_user_connections(username: str, db: Session = Depends(get_db)):
    connected_users = get_connections_for_user(username, db)
    return connected_users

@app.post("/users/{username}/connections")
def create_connection(username: str, connected_username: str, db: Session = Depends(get_db)):
    user1 = db.query(User).filter(User.name == username).first()
    user2 = db.query(User).filter(User.name == connected_username).first()
    
    if not user1 or not user2:
        raise HTTPException(status_code=404, detail="One or both users not found")
    if user1.id == user2.id:
        raise HTTPException(status_code=400, detail="A user cannot connect to themselves")
    
    user1_id, user2_id = sorted([user1.id, user2.id])
    existing_connection = db.query(UserConnection).filter(
        UserConnection.user1_id == user1_id,
        UserConnection.user2_id == user2_id
    ).first()
    
    if existing_connection:
        raise HTTPException(status_code=400, detail="Connection already exists")
    
    new_connection = UserConnection(user1_id=user1_id, user2_id=user2_id)
    db.add(new_connection)
    db.commit()
    return {"message": "Connection created", "user1": user1.name, "user2": user2.name}

@app.delete("/users/{username}/connections/{connected_username}")
def delete_connection(username: str, connected_username: str, db: Session = Depends(get_db)):
    user1 = db.query(User).filter(User.name == username).first()
    user2 = db.query(User).filter(User.name == connected_username).first()
    
    if not user1 or not user2:
        raise HTTPException(status_code=404, detail="One or both users not found")
    
    user1_id, user2_id = sorted([user1.id, user2.id])
    connection = db.query(UserConnection).filter(
        UserConnection.user1_id == user1_id,
        UserConnection.user2_id == user2_id
    ).first()
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    db.delete(connection)
    db.commit()
    return {"message": "Connection deleted", "user1": user1.name, "user2": connected_username}


RABBITMQ_HOST = "amqp://guest:guest@rabbitmq/"

async def on_request(message: aio_pika.IncomingMessage, connection: aio_pika.Connection):
    async with message.process():
        request_data = json.loads(message.body)
        username = request_data.get("username", "unknown")
        response = get_connections_for_user(username, next(get_db()))
        response = json.dumps([{"id": user.id, "name": user.name} for user in response])

        async with connection.channel() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=response.encode(),
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )


async def start_rabbitmq():
    retries = 5
    while retries > 0:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_HOST)
            channel = await connection.channel()
            queue = await channel.declare_queue("user_request")
            callback = partial(on_request, connection=connection)
            await queue.consume(callback)
            await asyncio.Future()
            break
        except aio_pika.exceptions.AMQPConnectionError as e:
            await asyncio.sleep(5)
            retries -= 1

asyncio.create_task(start_rabbitmq())