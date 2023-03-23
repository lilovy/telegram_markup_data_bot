import asyncio, datetime
from typing import Optional

from sqlalchemy import func, ForeignKey, UniqueConstraint, Boolean
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
        UniqueConstraint('project_name', 'user_id', name='unique_project_name'),
    )

    id: Mapped[str] = mapped_column(primary_key=True)
    mime_type_main: Mapped[str]
    linked_id: Mapped[Optional[str]]
    mime_type_second: Mapped[Optional[str]]
    project_name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    channel_id: Mapped[int] = mapped_column(default=int(CHANNEL_ID))


class Result(Base):
    __tablename__ = 'result'

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True,
        )
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    project_name: Mapped[str]
    file_name: Mapped[str] = mapped_column(unique=True)
    time_create: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
    )


# class RawData(Base):
#     __tablename__ = 'raw_data'

#     id: Mapped[int] = mapped_column(
#         primary_key=True,
#         autoincrement=True,
#     )
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
#     project_name: Mapped[str]
#     data_row: Mapped[str]
#     header: Mapped[bool] = mapped_column(default=False)
#     status: Mapped[bool] = mapped_column(default=False)
#     time_create: Mapped[datetime.datetime] = mapped_column(
#         server_default=func.now(),
#     )


class Data(Base):
    __tablename__ = 'data'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    project_name: Mapped[str]
    rows: Mapped[str]
    header: Mapped[bool] = mapped_column(default=False)
    tags: Mapped[Optional[str]]
    time_create: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
    )