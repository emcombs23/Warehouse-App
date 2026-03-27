from typing import Optional
from pathlib import Path

from sqlalchemy import Column, String, Integer, Float, Text, DateTime, text
from sqlmodel import SQLModel, Field, create_engine, Session


class Inventory(SQLModel, table=True):
    __tablename__ = "inventory"

    id: Optional[int] = Field(default=None, primary_key=True)
    sku: str = Field(sa_column=Column(String, nullable=False, unique=True))
    name: str = Field(sa_column=Column(String, nullable=False))
    category: Optional[str] = Field(default=None, sa_column=Column(String))
    size: Optional[str] = Field(default=None, sa_column=Column(String))
    color: Optional[str] = Field(default=None, sa_column=Column(String))
    quantity: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    location: Optional[str] = Field(default=None, sa_column=Column(String))
    supplier: Optional[str] = Field(default=None, sa_column=Column(String))
    cost: Optional[float] = Field(default=None, sa_column=Column(Float))
    price: Optional[float] = Field(default=None, sa_column=Column(Float))
    received_date: Optional[str] = Field(default=None, sa_column=Column(String))
    last_updated: Optional[str] = Field(default=None, sa_column=Column(DateTime, server_default=text('CURRENT_TIMESTAMP')))
    notes: Optional[str] = Field(default=None, sa_column=Column(Text))




engine = create_engine('sqlite:///warehouse_inventory.db')


