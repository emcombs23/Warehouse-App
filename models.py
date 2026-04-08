from typing import Optional
from pathlib import Path

from sqlalchemy import Column, String, Integer, Float, Text, DateTime, text
from sqlmodel import SQLModel, Field, create_engine, Session

class Inventory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    brand: str
    size: Optional[str] = None
    color: Optional[str] = None
    quantity: int
    price: float

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str

engine = create_engine('sqlite:///warehouse_inventory.db')
SQLModel.metadata.create_all(engine)

