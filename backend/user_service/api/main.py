from fastapi import FastAPI

app = FastAPI(root_path="/user")


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
def post_connection(username: str, connection_id: int):
    return {"message": f"Hello, {username}! You are viewing connection {connection_id}"}

@app.get("/users/{username}/connections/{connection_id}")
def get_connection(username: str, connection_id: int):
    return {"message": f"Hello, {username}! You are viewing connection {connection_id}"}

@app.delete("/users/{username}/connections/{connection_id}")
def delete_connection(username: str, connection_id: int):
    return {"message": f"Hello, {username}! You are viewing connection {connection_id}"}