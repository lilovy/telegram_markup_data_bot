from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=["users"]))
async def user_info(msg: Message):
    await msg.answer(
        'user info'
        )