'''
This code sets up a basic integration of FastAPI with SQLAlchemy to work with a MySQL database. 

'''
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker, Session
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root{password}@localhost:3306/coffee_shope")

SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False))

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
