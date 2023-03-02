from aiogram.types import Message
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_id: int):
        self.access_id = access_id
        super().__init__()

    async def on_process_message(self, msg: Message, _):
        if int(msg.from_user.id) != int(self.access_id):
            await msg.answer('Access Denied')
            raise CancelHandler()