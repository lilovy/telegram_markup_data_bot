from sqlalchemy import Column, String, BigInteger, DateTime, Integer
from src.db.db import Base, engine
from datetime import datetime
from src.db.db import create_db
from config import CHANNEL_ID


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(50))
    registration = Column(DateTime, default=datetime.now)
    permission = Column(String(20), default='user')

    def __init__(
        self, 
        user_id: int, 
        username: str, 
        permission: str = None
        ) -> None:

        self.user_id = user_id
        self.username = username
        self.permission = permission

    def __repr__(
        self
        ) -> str:

        info = f'<User: {self.user_id}>\n' \
            f'<Username: {self.username}>\n' \
            f'<Permission: {self.permission}>\n' \
            f'<Date of registration: {self.registration}>'
        return info


class Files(Base):
    __tablename__ = 'files'

    file_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    channel_id = Column(BigInteger, default=int(CHANNEL_ID))
    
    def __init__(
        self,
        file_id: int,
        user_id: int,
        channel_id: int = None
        ) -> None:
        self.file_id = file_id
        self.user_id = user_id
        self.channel_id = channel_id


create_db()