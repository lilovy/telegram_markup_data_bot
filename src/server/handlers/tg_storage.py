from aiogram import Router, F
from aiogram.types import Message, ContentType
from aiogram.methods import SendMessage
from aiogram.filters import Command
from aiogram.methods import (
    forward_message,
    send_message,
    )
from config import CHANNEL_ID

router = Router()


@router.message(Command(commands=['return']))
async def return_message(msg: Message):
    await forward_message.ForwardMessage(
        chat_id=msg.chat.id,
        from_chat_id=int(CHANNEL_ID),
        message_id=16,
    )


"""handler for save data in telegram cloud storage"""

# @router.message(F.document)
# async def save_document(msg: Message):
#     await msg.answer('save document...')
#     await forward_message.ForwardMessage(
#         chat_id=int(CHANNEL_ID),
#         from_chat_id=msg.chat.id,
#         message_id=msg.message_id,
#     )
#     await msg.answer('document saved!')