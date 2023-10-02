from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine =create_engine("sqlite:///db.db", echo=True)

def get_session():
    with Session(engine) as session:
        yield session

