from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import db


DB = db

engine = create_engine(f'sqlite:///{DB}')
session = sessionmaker(bind=engine)

Base =  declarative_base()

def create_db():
    Base.metadata.create_all(engine)