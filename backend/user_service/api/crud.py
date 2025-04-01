from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User, UserConnection

def create_user(username: str, db: Session):
    existing_user = db.query(User).filter(User.name == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(name=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "name": new_user.name}

def get_user_connections(username: str, db: Session):
    user = db.query(User).filter(User.name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    connections = db.query(UserConnection).filter(
        (UserConnection.user1_id == user.id) | (UserConnection.user2_id == user.id)
    ).all()
    
    connected_user_ids = {conn.user1_id if conn.user2_id == user.id else conn.user2_id for conn in connections}
    return db.query(User).filter(User.id.in_(connected_user_ids)).all()

async def create_connection(username: str, connected_username: str, db: Session):
    user1 = db.query(User).filter(User.name == username).first()
    user2 = db.query(User).filter(User.name == connected_username).first()

    if not user1 or not user2:
        raise HTTPException(status_code=404, detail="One or both users not found")
    if user1.id == user2.id:
        raise HTTPException(status_code=400, detail="A user cannot connect to themselves")

    user1_id, user2_id = sorted([user1.id, user2.id])
    if db.query(UserConnection).filter(UserConnection.user1_id == user1_id, UserConnection.user2_id == user2_id).first():
        raise HTTPException(status_code=400, detail="Connection already exists")

    new_connection = UserConnection(user1_id=user1_id, user2_id=user2_id)
    db.add(new_connection)
    db.commit()
    return {"message": "Connection created", "user1": user1.name, "user2": user2.name}

def delete_connection(username: str, connected_username: str, db: Session):
    user1 = db.query(User).filter(User.name == username).first()
    user2 = db.query(User).filter(User.name == connected_username).first()

    if not user1 or not user2:
        raise HTTPException(status_code=404, detail="One or both users not found")

    user1_id, user2_id = sorted([user1.id, user2.id])
    connection = db.query(UserConnection).filter(
        UserConnection.user1_id == user1_id, UserConnection.user2_id == user2_id
    ).first()

    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    db.delete(connection)
    db.commit()
    return {"message": "Connection deleted", "user1": user1.name, "user2": connected_username}
