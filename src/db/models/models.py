from sqlalchemy import Column, String, BigInteger, DateTime
from src.db.db import Base, engine
from datetime import datetime
from src.db.db import create_db


class User(Base):
    __tablename__ = 'users'

    userid = Column(BigInteger, primary_key=True)
    username = Column(String(50))
    registration = Column(DateTime, default=datetime.now)

    def __init__(self, userid: int, username: str):
        self.userid = userid
        self.username = username

    def __repr__(self) -> str:
        info = f'{self.userid}\n' \
            f'{self.username}\n' \
            f'{self.registration}'
        return info


# class


create_db()