from sqlmodel import Session, select
from models import Inventory, engine

with Session(engine) as session:
    statement = select(Inventory).where(Inventory.id== 1)
    results = session.exec(statement).one()

    print(results)
    print(results.quantity)
    results.quantity += 30
    print(results.quantity)
    
    session.add(results)
    session.commit()
    session.refresh(results)