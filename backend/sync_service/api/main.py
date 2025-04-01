from fastapi import FastAPI
from rabbitmq import send_user_request, send_meal_request

app = FastAPI(root_path="/sync")

@app.get("/{username}/synced_meals")
async def get_synced_meals(username: str):
    user_data = await send_user_request(username)

    all_meals_with_owner = []

    meal_data = await send_meal_request(username)
    for meal in meal_data:
        meal["owner"] = username
    all_meals_with_owner.extend(meal_data)

    for user in user_data:
        if user["name"] != username:
            meal_data = await send_meal_request(user["name"])
            for meal in meal_data:
                meal["owner"] = user["name"]
            all_meals_with_owner.extend(meal_data)

    return all_meals_with_owner


