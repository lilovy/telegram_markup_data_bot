import asyncio
from .db_async import create_db
from .models.async_models import User, File


def init_db():
    asyncio.run(create_db())
