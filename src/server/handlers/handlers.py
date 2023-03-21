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

@router.message(Command(commands=["start"]))
@router.message(F.text.casefold() == 'start')
async def welcome(msg: Message):
    await msg.answer(
        'Hello!\n\n' \
        'this bot will help you to manually markup\n' \
        'data for neural network training\n\n' \
        'to start markup /run\n\n' \
        'for more information /help\n\n' \
        'contact @trump for full access' \
        )


@router.message(Command(commands=['help']))
@router.message(F.text.casefold() == 'help')
async def help(msg: Message):
    await msg.answer('bot for manual markup data')
