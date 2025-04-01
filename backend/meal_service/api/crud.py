from sqlalchemy.orm import Session
from models import Meal, Ingredient

def get_user_meals(username: str, db: Session):
    return db.query(Meal).filter(Meal.username == username).all()

def create_meal(username: str, name: str, date, db: Session):
    new_meal = Meal(name=name, username=username, planned_for=date)
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    return new_meal

def delete_meal(username: str, meal_id: int, db: Session):
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.username == username).first()
    if meal:
        db.delete(meal)
        db.commit()
        return True
    return False

def get_meal_by_id(username: str, meal_id: int, db: Session):
    return db.query(Meal).filter(Meal.id == meal_id, Meal.username == username).first()

def create_ingredient(meal_id: int, name: str, amount: str, db: Session):
    new_ingredient = Ingredient(meal_id=meal_id, name=name, amount=amount)
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient
