from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.db.action import check_unique_file_name


access_mime_type = [
    'text/csv', 
    'text/plain', 
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
]

class MIMEType(BaseFilter):
    async def __call__(
        self,
        msg: Message,
        ) -> bool:
        
        if msg.document.mime_type in access_mime_type:
            return True
        else:
            await msg.answer(
                'Please use (.csv, .txt, .xls, .xlsx) file'
                )
            return False


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