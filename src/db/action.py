from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    AsyncScalarResult,
)
from sqlalchemy.future import select
from sqlalchemy import delete
from .db_async import async_session
from .models.async_models import User, File, RawData
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


async def get_file_mimetype(
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

    return (result.mime_type_main, result.mime_type_second)


async def get_data_row(
    user_id: int,
    project_name: str
    ) -> list[str]:
    
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(RawData).where(
                RawData.user_id == user_id,
                RawData.project_name == project_name,
                RawData.status is not True,
                )
            result = await session.scalars(stmt)
        
    rows: list = []
    for row in result:
        row: RawData
        # if not row.status:
        rows.append(row.data_row)


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
    mime_type_main: str,
    linked_file_id: int,
    mime_type_second: str,
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
                    mime_type_main=mime_type_main,
                    linked_id=linked_file_id,
                    mime_type_second=mime_type_second,
                    channel_id=channel_id,
                    )
                await session.merge(file)
    except Exception as e:
        raise e


async def save_file_data(
    user_id: int,
    project_name: str,
    data: list,
) -> None:
    try: 
        async with async_session() as session: 
            session: AsyncSession
            async with session.begin():
                rows = []
                for row in data:
                    file = RawData(
                        user_id=user_id,
                        project_name=name,
                        data_row=row,
                        )
                    session.d
                    rows.append(file)
                session.add_all(rows)
                session.commit()
    except Exception as e:
        raise e


async def update_file_data(
    user_id: int,
    project_name: str,
    row: str,
) -> None:
    try: 
        async with async_session() as session: 
            session: AsyncSession
            async with session.begin():
                file = RawData(
                    user_id=user_id,
                    project_name=name,
                    data_row=row,
                    )
                file.status = True
                session.merge(file)
    except Exception as e:
        raise e


async def del_file_data(
    user_id: int,
    project_name: str,
) -> None:
    try: 
        async with async_session() as session:
            session: AsyncSession
            async with session.begin():
                stmt = select(RawData).where(
                    RawData.user_id == user_id,
                    RawData.project_name == project_name,
                    )
                result = await session.scalars(stmt)
                for row in result:
                    await session.delete(row)
                await session.commit()


async def check_exist_data(
    user_id: int,
    project_name: str,
    ) -> bool:
    """
    file exist check
    
    if row data exist -> return True
    else -> return False
    """
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(RawData).where(
                RawData.user_id == user_id, 
                RawData.project_name == name,
                )
            file: RawData = await session.scalar(stmt)

    if file:
        return True
    
    return False