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
async def welcome(msg: Message):
    await msg.answer('salem')


@router.message(Command(commands=['help']))
async def help(msg: Message):
    await msg.answer('bot for manual markup data')
