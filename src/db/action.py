import re
from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    AsyncScalarResult,
)
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.engine import ScalarResult
from .db_async import async_session
from .models.async_models import User, File, Data, Result
from config import CHANNEL_ID
from .db_async import Base


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


async def get_data_rows(
    user_id: int,
    project_name: str
    ) -> list[str]:

    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(Data).where(
                Data.user_id == user_id,
                Data.project_name == project_name,
                Data.tags is None,
                ).order_by(
                    Data.time_create)
            result = await session.scalars(stmt)
        
    rows: list = []
    # rows = [row.data_row for row in result if row.status]
    for row in result:
        row: Data
        # if not row.status:
        rows.append(row.rows)
    return rows


async def get_data_row(
    user_id: int,
    project_name: str
    ) -> str:

    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(Data).where(
                Data.user_id == user_id,
                Data.project_name == project_name,
                Data.tags == None,
                Data.header == False,
                ).order_by(
                    Data.time_create,
                )
            result = await session.scalars(stmt)

    row: Data = result.first()
    if row:
        return row.rows
    return


async def get_header(
    user_id: int,
    project_name: str,
) -> str:
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(Data).where(
                Data.user_id == user_id,
                Data.project_name == project_name,
                Data.header == True,
            )
            result: Data = await session.scalar(stmt)
    return result.rows


async def get_result_filename(
    user_id: int,
    project_name: str,
) -> str:
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(Result).where(
                Result.user_id == user_id,
                Result.project_name == project_name,
            )
            result: Result = await session.scalar(stmt)
    return result.file_name


async def get_marked_data(
    user_id: int,
    project_name: str,
) -> list:
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            stmt = select(Data).where(
                Data.user_id == user_id,
                Data.project_name == project_name,
                # Data.header == True,
            ).order_by(Data.time_create)
            result: ScalarResult[Data] = await session.scalars(stmt)
        
    rows = []
    
    for row in result:
        print(row.rows)
        raw_row = row.rows
        sep = re.findall(r'[^\w\s]+', raw_row)[0]
        res = raw_row + sep + row.tags + '\n'
        rows.append(res)
    
    return rows


async def check_unique_file_name(
    user_id: int,
    name: str,
    ) -> bool:
    """
    name uniqueness check
    
    if the name is unique -> return True
    else -> return False
    """
    try:
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
    except Exception as e:
        raise e


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


async def save_result_filename(
    user_id: int,
    project_name: str,
    filename: str,
    ) -> None:
    try:
        async with async_session() as session:
            session: AsyncSession
            async with session.begin():
                file_name = Result(
                    user_id=user_id,
                    project_name=project_name,
                    file_name=filename,
                )
                await session.merge(file_name)
        # return user
    except Exception as e:
        raise e


async def save_file_data(
    user_id: int,
    project_name: str,
    data: list,
    # header: bool = False,
) -> None:

    try: 
        async with async_session() as session: 
            session: AsyncSession
            async with session.begin():

                rows = []
                for i, row in enumerate(data):
                    header = False
                    header_tag = None
                    if i == 0:
                        header = True
                        header_tag = 'marked_column'

                    file = Data(
                        user_id=user_id,
                        project_name=project_name,
                        rows=row[0],
                        header=header,
                        tags=header_tag,
                        )

                    rows.append(file)
                session.add_all(rows)
                # session.commit()
    except Exception as e:
        raise e


# async def update_file_data_status(
#     user_id: int,
#     project_name: str,
#     row: str,
# ) -> None:
#     try: 
#         async with async_session() as session: 
#             session: AsyncSession
#             async with session.begin():
#                 file = Data(
#                     user_id=user_id,
#                     project_name=name,
#                     data_row=row,
#                     )
#                 file.status = True
#                 session.merge(file)
#     except Exception as e:
#         raise e


async def add_data_tags(
    user_id: int,
    project_name: str,
    row: str,
    tags: str,
) -> None:
    try: 
        async with async_session() as session: 
            session: AsyncSession
            async with session.begin():
                # file = Data(
                #     user_id=user_id,
                #     project_name=project_name,
                #     rows=row,
                #     )
                stmt = select(Data).where(
                    Data.user_id == user_id,
                    Data.project_name == project_name,
                    Data.rows == row,
                )
                
                result: Data = await session.scalar(stmt)
                result.tags = tags
                await session.merge(result)
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
                stmt = select(Data).where(
                    Data.user_id == user_id,
                    Data.project_name == project_name,
                    )
                result = await session.scalars(stmt)
                for row in result:
                    await session.delete(row)
                await session.commit()
    except Exception as e:
        raise e


async def check_exist_data(
    user_id: int,
    project_name: str,
    table: Base = Data
    ) -> bool:
    """
    file exist check
    
    if data exist -> return True
    else -> return False
    """
    try:
        async with async_session() as session:
            session: AsyncSession
            async with session.begin():
                stmt = select(table).where(
                    table.user_id == user_id, 
                    table.project_name == project_name,
                    )
                file: table = await session.scalar(stmt)

        if file:
            return True
        
        return False
    except Exception as e:
        raise e