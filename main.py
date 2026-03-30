from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from sqlmodel import Session, select
from models import Inventory, engine

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
        result = session.exec(statement).one()
        if result:
            session.delete(result)
            session.commit()

app.mount("/", StaticFiles(directory="static", html=True), name="static")