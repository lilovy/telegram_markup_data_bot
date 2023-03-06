from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.methods import SendMessage

router = Router()


@router.message(F.text)
async def echo(msg: Message):

    await msg.answer(msg.text)
