from sqlmodel import Session, select
from models import Inventory, engine


with Session(engine) as session:
    statement = select(Inventory)

    results = session.exec(statement).all()
    print(results)
