from src.db.action import (
    check_unique_file_name,
    get_user_info,
    get_user_files
    )
import asyncio


async def run():
    print(await get_user_files(user_id=653053151))


asyncio.run(run())

