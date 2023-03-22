from src.db import action
import asyncio


async def run():
    print(
        await action.get_data_row(
            user_id=653053151,
            project_name='first',
            )
        )


asyncio.run(run())

