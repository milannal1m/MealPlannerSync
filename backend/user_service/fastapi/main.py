from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/users")
def create_user(username: str):
    return {"message": f"Created user {username}"}


@app.get("/users/{username}/connections")
def get_connections(username: str):
    return {"message": f"Hello, {username}! You are viewing your connections"}

@app.post("/users/{username}/connections")
def get_connection(username: str, connection_id: int):
    return {"message": f"Hello, {username}! You are viewing connection {connection_id}"}

@app.get("/users/{username}/connections/{connection_id}")
def get_connection(username: str, connection_id: int):
    return {"message": f"Hello, {username}! You are viewing connection {connection_id}"}

@app.delete("/users/{username}/connections/{connection_id}")
def get_connection(username: str, connection_id: int):
    return {"message": f"Hello, {username}! You are viewing connection {connection_id}"}