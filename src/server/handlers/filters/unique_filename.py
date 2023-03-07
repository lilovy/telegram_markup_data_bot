from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message

from ....db.action import check_unique_file_name


class UniqueFileName(BaseFilter):
    async def __call__(
        self,
        msg: Message,
        ) -> Union[bool, Dict[str, Any]]:
        if await check_unique_file_name(
            user_id=msg.chat.id,
            name=msg.text,
            ):
            return {'name': msg.text}
        else:
            await msg.answer(
                'This name is already used'
            )
            return False