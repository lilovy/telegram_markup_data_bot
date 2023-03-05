import asyncio, datetime

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    )
from sqlalchemy.orm import declarative_base
from config import db_path

Base = declarative_base()
engine = create_async_engine(
    url=f"sqlite+aiosqlite:///{db_path}"
    )
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_db():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
            )
