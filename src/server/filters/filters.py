from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message

from ...db.action import check_unique_file_name


access_mime_type = {
    "data": [
        'text/csv', 
        'application/json',
        'text/plain',
        # 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        # 'application/vnd.ms-excel',
    ],
    'categories' : [
        'text/plain',
    ],
}

class MIMEType(BaseFilter):
    def __init__(
        self,
        mime_access: Union[str, list],
        ):
        super().__init__()
        self.mime_access = mime_access

    async def __call__(
        self,
        msg: Message,
        ) -> bool:
        
        if msg.document.mime_type in self.mime_access:
            return True
        else:
            await msg.answer(
                'Please use (.csv, .txt, .json) for target file\n' \
                'and (.txt) for category file'
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