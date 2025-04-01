from fastapi import FastAPI, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio
from db import get_db
from rabbitmq import send_notification, start_sync_queue, start_websocket_queue
from crud import get_user_meals, create_meal, delete_meal, get_meal_by_id, create_ingredient

app = FastAPI(root_path="/meal")

asyncio.create_task(start_sync_queue())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await start_websocket_queue(websocket)

@app.get("/{username}/meals")
def get_meals(username: str, db: Session = Depends(get_db)):
    meals = get_user_meals(username, db)
    if not meals:
        raise HTTPException(status_code=404, detail="No meals found for this user")
    return {"meals": [{"id": meal.id, "name": meal.name, "planned_for": meal.planned_for} for meal in meals]}


@app.post("/{username}/meals")
async def create_meal_endpoint(username: str, name: str, date: datetime, db: Session = Depends(get_db)):
    new_meal = create_meal(username, name, date, db)
    await send_notification(f"New Meal {new_meal.id}")
    return new_meal


@app.delete("/{username}/meals/{meal_id}")
def delete_meal_endpoint(username: str, meal_id: int, db: Session = Depends(get_db)):
    if not delete_meal(username, meal_id, db):
        raise HTTPException(status_code=404, detail="Meal not found")
    return {"message": f"Deleted meal {meal_id}"}


@app.get("/{username}/meals/{meal_id}/ingredients")
def get_ingredients(username: str, meal_id: int, db: Session = Depends(get_db)):
    meal = get_meal_by_id(username, meal_id, db)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return [{"id": ing.id, "name": ing.name, "amount": ing.amount} for ing in meal.ingredients]


@app.post("/{username}/meals/{meal_id}/ingredients")
def create_ingredient_endpoint(username: str, meal_id: int, name: str, amount: str, db: Session = Depends(get_db)):
    meal = get_meal_by_id(username, meal_id, db)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    new_ingredient = create_ingredient(meal_id, name, amount, db)
    return {"id": new_ingredient.id, "name": new_ingredient.name, "amount": new_ingredient.amount}