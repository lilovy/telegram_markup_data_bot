import asyncio, datetime
from typing import Optional

from sqlalchemy import func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    )
from ..db_async import Base
from config import CHANNEL_ID


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]]
    permission: Mapped[Optional[str]] = mapped_column(default='guest')
    registration: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )


class File(Base):
    __tablename__ = 'file'
    __table_args__ = (
        UniqueConstraint('projectname', 'user_id', name='project_name'),
    )

    id: Mapped[str] = mapped_column(primary_key=True)
    linked_id: Mapped[Optional[str]]
    projectname: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    channel_id: Mapped[int] = mapped_column(default=int(CHANNEL_ID))