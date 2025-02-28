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


@app.get("/{username}/synced_meals")
def get_synced_meals(username: str):
    return {"username": username, "meals": []}
