from aiogram import Router, F
from aiogram.types import Message
from aiogram.methods import SendMessage

router = Router()


@router.message(F.text)
async def echo(msg: Message):

    return SendMessage(
        chat_id=msg.chat.id, 
        text=msg.text,
        )