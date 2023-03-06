from sqlalchemy.ext.asyncio import (
    AsyncSession
)
from sqlalchemy.future import select
from .db_async import async_session
from .models.async_models import User, File



async def get_user_files(user_id: int):
    
    async with async_session() as session:
        session: AsyncSession
        stmt = select(File).where(File.user_id == user_id)
        result = await session.scalar(stmt)
        
        file_ids: list
        for f in result:
            f: File
            file_ids.append(f.id)

    return file_ids

async def get_user_permission(user_id: int):

    permission = 'guest'
    
    try:
        async with async_session() as session:
            session: AsyncSession
            stmt = select(User).where(User.id == user_id)
            result: list[User] = await session.scalar(stmt)

            permission: str = result[0].permission

    except Exception as e:
        raise e

    return permission
