from fastapi import FastAPI, Depends, HTTPException, WebSocket
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from datetime import datetime
import aio_pika
import asyncio
from functools import partial
import json
from aio_pika import Message, DeliveryMode, connect_robust


dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')
load_dotenv()

postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_user = os.getenv("POSTGRES_USER")

engine = create_engine(f"postgresql://{postgres_user}:{postgres_password}@meal-postgres:5432/meal_db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(root_path="/meal")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_rabbitmq_connection():
    return await connect_robust("amqp://guest:guest@rabbitmq/")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
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

async def send_notification(message: str):
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    exchange = await channel.declare_exchange("notifications", aio_pika.ExchangeType.FANOUT)

    await exchange.publish(
        Message(message.encode(), delivery_mode=DeliveryMode.PERSISTENT),
        routing_key=""
    )
    await connection.close()

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    planned_for = Column(DateTime, nullable=True)
    ingredients = relationship("Ingredient", back_populates="meal", cascade="all, delete-orphan")

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    amount = Column(String)
    meal = relationship("Meal", back_populates="ingredients")

def get_user_meals(username: str, db: Session):
    return db.query(Meal).filter(Meal.username == username).all()

@app.get("/{username}/meals")
def get_meals(username: str, db: Session = Depends(get_db)):
    meals = get_user_meals(username, db)
    if not meals:
        raise HTTPException(status_code=404, detail="No meals found for this user")
    return {"meals": [{"id": meal.id, "name": meal.name, "planned_for": meal.planned_for} for meal in meals]}

@app.post("/{username}/meals")
async def create_meal(username: str, name:str, date:datetime, db: Session = Depends(get_db)):   
    new_meal = Meal(name=name , username=username, planned_for=date)
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    await send_notification("New Meal" + str(new_meal.id))
    return new_meal

@app.delete("/{username}/meals/{meal_id}")
def delete_meal(username: str, meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.username == username).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    db.delete(meal)
    db.commit()
    return {"message": f"Deleted meal {meal_id}"}

@app.get("/{username}/meals/{meal_id}/ingredients")
def get_ingredients(username: str, meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.username == username).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    return [{"id": ing.id, "name": ing.name, "amount": ing.amount} for ing in meal.ingredients]

@app.post("/{username}/meals/{meal_id}/ingredients")
def create_ingredient(username: str, meal_id: int, name: str, amount: str, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.username == username).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    new_ingredient = Ingredient(meal_id=meal_id, name=name, amount=amount)
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    
    return {"id": new_ingredient.id, "name": new_ingredient.name, "amount": new_ingredient.amount}

@app.delete("/{username}/meals/{meal_id}/ingredients/{ingredient_id}")
def delete_ingredient(username: str, meal_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id, Ingredient.meal_id == meal_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    db.delete(ingredient)
    db.commit()
    return {"message": f"Deleted ingredient {ingredient_id}"}

async def on_request(message: aio_pika.IncomingMessage, connection: aio_pika.Connection):
    async with message.process():
        request_data = json.loads(message.body)
        username = request_data.get("username", "unknown")
        response = get_user_meals(username, next(get_db()))
        response = json.dumps([{"id": meal.id, "name": meal.name, "planned_for": meal.planned_for.isoformat()} for meal in response])

        async with connection.channel() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=response.encode(),
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )

async def start_sync_queue():
    retries = 5
    while retries > 0:
        try:
            connection = await get_rabbitmq_connection
            channel = await connection.channel()
            queue = await channel.declare_queue("meal_request")
            callback = partial(on_request, connection=connection)
            await queue.consume(callback)
            await asyncio.Future()
            break
        except aio_pika.exceptions.AMQPConnectionError as e:
            await asyncio.sleep(5)
            retries -= 1

asyncio.create_task(start_sync_queue())