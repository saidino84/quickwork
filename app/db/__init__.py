from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db.models import Product,Base,Supplier,User

engine =create_engine("sqlite:///db.db", echo=True)
Base.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

