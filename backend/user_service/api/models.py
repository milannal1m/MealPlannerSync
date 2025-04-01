from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class UserConnection(Base):
    __tablename__ = "user_connections"
    user1_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user2_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
