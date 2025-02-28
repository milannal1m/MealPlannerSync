from pydantic import BaseModel
from typing import List
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

class Ingredient(BaseModel):
    name: str
    quantity: int

class Meal(BaseModel):
    name: str
    ingredients: List[Ingredient]


@app.get("/{username}/meals")
def get_meals(username: str):
    return {"message": f"Hello, {username}!"}

@app.post("/{username}/meals")
def create_meal(username: str, meal: Meal):
    return {"message": f"Created meal"}

@app.get("/{username}/meals/{meal_id}")
def get_meal(username: str, meal_id: int):
    return {"message": f"Hello, {username}! You are viewing meal {meal_id}"}

@app.put("/{username}/meals/{meal_id}")
def update_meal(username: str, meal_id: int, meal: Meal):
    return {"message": f"Updated meal {meal_id}"}

@app.delete("/{username}/meals/{meal_id}")
def delete_meal(username: str, meal_id: int):
    return {"message": f"Deleted meal {meal_id}"}

@app.get("/{username}/meals/{meal_id}/ingredients")
def get_ingredients(username: str, meal_id: int):
    return {"message": f"Hello, {username}! You are viewing ingredients for meal {meal_id}"}

@app.get("/{username}/meals/{meal_id}/ingredients/{ingredient_id}")
def get_ingredient(username: str, meal_id: int, ingredient_id: int):
    return {"message": f"Hello, {username}! You are viewing ingredient {ingredient_id}"}

@app.put("/{username}/meals/{meal_id}/ingredients/{ingredient_id}")
def update_ingredient(username: str, meal_id: int, ingredient_id: int):
    return {"message": f"Hello, {username}! You are updating ingredient {ingredient_id}"}

@app.delete("/{username}/meals/{meal_id}/ingredients/{ingredient_id}")
def delete_ingredient(username: str, meal_id: int, ingredient_id: int):
    return {"message": f"Hello, {username}! You are deleting ingredient {ingredient_id}"}