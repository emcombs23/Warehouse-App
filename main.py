from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from models import Inventory,User, engine
import bcrypt
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

app = FastAPI()


@app.get("/inventory")
async def get_inventory():
    with Session(engine) as session:
        statement = select(Inventory)
        results = session.exec(statement).all()
        return results


@app.delete('/inventory/{id}')
async def delete_inventory(id: int):
    with Session(engine) as session:
        statement = select(Inventory).where(Inventory.id == id)
        record = session.exec(statement).one()
        session.delete(record)
        session.commit()

@app.post("/inventory")
async def create_item(item: Inventory):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

@app.put("/update/{id}")
async def update_item(id: int, item: Inventory):
    with Session(engine) as session:
        statement = select(Inventory).where(Inventory.id == id)
        record = session.exec(statement).one()
        record.name = item.name
        record.category = item.category
        record.brand = item.brand
        record.size = item.size
        record.color = item.color
        record.quantity = item.quantity
        record.price = item.price
        session.add(record)
        session.commit()
        session.refresh(record)
        return record


@app.post("/register")
async def register(user: UserCreate):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        user_record = User(username=user.username, password_hash=hash_password(user.password))
        session.add(user_record)
        session.commit()
        session.refresh(user_record)
        return {"id": user_record.id, "username": user_record.username, 'password_hash': user_record.password_hash}


@app.post("/login")
async def login(user: UserCreate):
    with Session(engine) as session:
        user_record = session.exec(select(User).where(User.username == user.username)).first()
        if not user_record or not bcrypt.checkpw(user.password.encode(), user_record.password_hash.encode()):
            raise HTTPException(status_code=400, detail="Invalid username or password")
        return {"message": "Login successful", "username": user_record.username}

app.mount("/", StaticFiles(directory="static", html=True), name="static")