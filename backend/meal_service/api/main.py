from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')
load_dotenv()

postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_user = os.getenv("POSTGRES_USER")

engine = create_engine(f"postgresql://{postgres_user}:{postgres_password}@meal-postgres:5432/meal_db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test-db-connection")
def test_db_connection():
    try:
        # Öffne eine Sitzung und führe eine einfache Abfrage durch
        with SessionLocal() as session:
            # Führe eine einfache SQL-Abfrage durch, um zu testen, ob die Verbindung funktioniert
            result = session.execute(text("SELECT 1")).scalar()

            if result == 1:
                return {"status": "success", "message": "Verbindung zur Datenbank erfolgreich!"}
            else:
                return {"status": "failure", "message": "Testabfrage fehlgeschlagen!"}

    except OperationalError as e:
        return {"status": "failure", "message": f"Fehler beim Verbinden mit der Datenbank: {str(e)}"}

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