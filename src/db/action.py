from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    AsyncScalarResult,
)
from sqlalchemy.future import select
from .db_async import async_session
from .models.async_models import User, File
from config import CHANNEL_ID


async def get_user_info(
    user_id: int,
    ) -> User:
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(User).where(User.id == user_id)
            user: User = await session.scalar(stmt)

    return user



async def get_user_filenames(
    user_id: int,
    ) -> list[str]:
    
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(File).where(
                File.user_id == user_id,
                )
            result = await session.scalars(stmt)
        
    file_ids: list = []
    for f in result:
        f: File
        file_ids.append(f.project_name)

    return file_ids

async def get_user_file(
    user_id: int,
    project_name: str,
    ) -> tuple[str, str]:
    
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(File).where(
                File.user_id == user_id,
                File.project_name == project_name,
                )
            result: File = await session.scalar(stmt)

    return (result.id, result.linked_id)


async def get_user_permission(
    user_id: int,
    ) -> str:

    try:
        async with async_session() as session:
            session: AsyncSession
            stmt = select(User).where(User.id == user_id)
            user: User = await session.scalar(stmt)

            permission: str = user.permission
        return permission

    except Exception as e:
        raise e



async def check_unique_file_name(
    user_id: int,
    name: str,
    ) -> bool:
    """
    name uniqueness check
    
    if the name is unique -> return True
    else -> return False
    """
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(File).where(
                File.user_id == user_id, 
                File.project_name == name,
                )
            file: File = await session.scalar(stmt)

    if file:
        return False
    else:
        return True


async def save_user(
    user_id: int,
    username: str,
    permission: str = None,
    ) -> None:
    try:
        async with async_session() as session:
            session: AsyncSession
            async with session.begin():
                user = User(
                    id=user_id,
                    username=username,
                    permission=permission,
                )
                await session.merge(user)
        return user
    except Exception as e:
        raise e

async def save_file_info(
    user_id: int,
    name: str,
    id: int,
    linked_file_id: int,
    channel_id: int = CHANNEL_ID,
    ) -> None:
    try: 
        async with async_session() as session: 
            session: AsyncSession
            async with session.begin():
                file = File(
                    user_id=user_id,
                    project_name=name,
                    id=id,
                    linked_id=linked_file_id,
                    channel_id=channel_id,
                    )
                await session.merge(file)
    except Exception as e:
        raise e